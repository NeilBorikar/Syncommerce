from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import io
from app.api.deps import get_db, get_current_user, require_role
from app.schemas.branch_schema import BranchCreate, BranchUpdate
from app.services.branch_service import BranchService

router = APIRouter()

owner_only = Depends(require_role(["owner"]))

@router.post("/", dependencies=[owner_only])
def create_branch(data: BranchCreate, db=Depends(get_db)):
    service = BranchService(db)
    return service.create_branch(data.model_dump())

@router.get("/{business_id}")
def list_branches(business_id: str, db=Depends(get_db)):
    service = BranchService(db)
    return service.get_by_business(business_id)

@router.put("/{id}", dependencies=[owner_only])
def update_branch(id: str, data: BranchUpdate, db=Depends(get_db)):
    service = BranchService(db)
    return service.update_branch(id, data.model_dump(exclude_unset=True))
