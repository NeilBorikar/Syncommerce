import io
from typing import Optional, Dict
from openpyxl import Workbook
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password
from app.utils.logger import logger


# Role hierarchy: higher index = higher privilege
ROLE_HIERARCHY = {"worker": 0, "manager": 1, "owner": 2}


class EmployeeService:
    def __init__(self, db):
        self.repo = UserRepository(db)

    # -------------------------------
    # ADD EMPLOYEE (RBAC)
    # -------------------------------
    def add_employee(self, data: dict, requesting_user: dict) -> Dict:
        """
        Owner can add any role (manager or worker).
        Manager can only add workers.
        """
        try:
            requester_role = requesting_user.get("role", "worker")
            target_role = data.get("role", "worker")

            if ROLE_HIERARCHY.get(requester_role, 0) < ROLE_HIERARCHY.get(target_role, 0):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"A {requester_role} cannot add a {target_role}",
                )

            # Manager can only add workers
            if requester_role == "manager" and target_role != "worker":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Managers can only add workers",
                )

            existing = self.repo.get_by_email(data["email"])
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists",
                )

            employee_data = {k: v for k, v in data.items() if k != "password"}
            employee_data["hashed_password"] = hash_password(data["password"])
            employee_data["is_active"] = True
            employee_data["status"] = "active"

            # Inherit business_id from requesting user if not explicitly provided
            if not employee_data.get("business_id"):
                employee_data["business_id"] = requesting_user.get("business_id")

            created = self.repo.create(employee_data)
            logger.info(f"Employee created: {created['id']} by {requesting_user.get('id')}")
            return {k: v for k, v in created.items() if k != "hashed_password"}

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Employee creation failed", exc_info=True)
            raise e

    # -------------------------------
    # UPDATE EMPLOYEE (RBAC)
    # -------------------------------
    def update_employee(
        self,
        employee_id: str,
        data: dict,
        requesting_user: dict,
    ) -> Optional[Dict]:
        """
        Owner can update anyone.
        Manager can only update workers (not other managers or owners).
        """
        try:
            requester_role = requesting_user.get("role", "worker")
            target = self.repo.get_by_id(employee_id)

            if not target:
                raise HTTPException(status_code=404, detail="Employee not found")

            target_role = target.get("role", "worker")

            # RBAC: manager cannot edit managers or owners
            if requester_role == "manager" and target_role != "worker":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Managers can only update workers",
                )

            if requester_role == "worker":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Workers cannot update other employees",
                )

            clean_data = {k: v for k, v in data.items() if v is not None}

            if "password" in clean_data:
                clean_data["hashed_password"] = hash_password(clean_data.pop("password"))

            updated = self.repo.update(employee_id, clean_data)
            logger.info(f"Employee updated: {employee_id}")
            return {k: v for k, v in (updated or {}).items() if k != "hashed_password"}

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Employee update failed", exc_info=True)
            raise e

    # -------------------------------
    # DELETE EMPLOYEE (RBAC)
    # -------------------------------
    def delete_employee(self, employee_id: str, requesting_user: dict) -> Dict:
        """Owner only can delete employees."""
        try:
            requester_role = requesting_user.get("role", "worker")
            if requester_role != "owner":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only owners can delete employees",
                )

            target = self.repo.get_by_id(employee_id)
            if not target:
                raise HTTPException(status_code=404, detail="Employee not found")

            deleted = self.repo.delete(employee_id)
            if not deleted:
                raise HTTPException(status_code=500, detail="Delete failed")

            logger.info(f"Employee deleted: {employee_id}")
            return {"deleted": True, "employee_id": employee_id}

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Employee delete failed", exc_info=True)
            raise e

    # -------------------------------
    # SUSPEND / ACTIVATE EMPLOYEE
    # -------------------------------
    def suspend_employee(
        self,
        employee_id: str,
        new_status: str,
        requesting_user: dict,
    ) -> Optional[Dict]:
        """
        Owner or manager can suspend/activate workers.
        Only owner can change manager status.
        """
        try:
            requester_role = requesting_user.get("role", "worker")
            if requester_role == "worker":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Workers cannot change employee status",
                )

            target = self.repo.get_by_id(employee_id)
            if not target:
                raise HTTPException(status_code=404, detail="Employee not found")

            target_role = target.get("role", "worker")
            if requester_role == "manager" and target_role != "worker":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Managers can only change worker status",
                )

            is_active = new_status == "active"
            updated = self.repo.update(
                employee_id, {"status": new_status, "is_active": is_active}
            )
            logger.info(f"Employee {employee_id} status set to {new_status}")
            return {k: v for k, v in (updated or {}).items() if k != "hashed_password"}

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Employee status update failed", exc_info=True)
            raise e

    # -------------------------------
    # LIST EMPLOYEES
    # -------------------------------
    def list_employees(self, business_id: str):
        employees = self.repo.get_by_business(business_id)
        return [{k: v for k, v in e.items() if k != "hashed_password"} for e in employees]

    # -------------------------------
    # EXPORT TO EXCEL
    # -------------------------------
    def export_excel(self, business_id: str) -> bytes:
        """Generate an Excel workbook with all employee data."""
        try:
            employees = self.repo.get_by_business(business_id)

            wb = Workbook()
            ws = wb.active
            ws.title = "Employees"

            headers = [
                "ID", "Name", "Email", "Role", "Phone",
                "Salary", "Date Joined", "Branch ID",
                "Status", "Is Active", "Created At",
            ]
            ws.append(headers)

            for e in employees:
                ws.append([
                    e.get("id", ""),
                    e.get("name", ""),
                    e.get("email", ""),
                    e.get("role", ""),
                    e.get("phone", ""),
                    e.get("salary", 0),
                    e.get("date_joined", ""),
                    e.get("branch_id", ""),
                    e.get("status", "active"),
                    e.get("is_active", True),
                    str(e.get("created_at", "")),
                ])

            buffer = io.BytesIO()
            wb.save(buffer)
            buffer.seek(0)
            return buffer.read()

        except Exception as e:
            logger.error("Employee Excel export failed", exc_info=True)
            raise e
