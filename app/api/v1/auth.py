from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schema import UserCreate
from app.schemas.business_schema import BusinessRegistrationPayload, BusinessLoginPayload
from app.repositories.user_repository import UserRepository
from app.repositories.business_repository import BusinessRepository
from app.models.business_model import Business
from app.models.user_model import User
from app.core.security import hash_password, verify_password, create_access_token
from app.api.deps import get_db
import uuid


router = APIRouter()


@router.post("/business/register")
def register_business(payload: BusinessRegistrationPayload, db=Depends(get_db)):
    bus_repo = BusinessRepository(db)
    user_repo = UserRepository(db)

    # Check if business email exists
    if bus_repo.get_by_email(payload.business.email):
        raise HTTPException(400, "Business email already exists")
    
    # Check if owner email exists
    if user_repo.get_by_email(payload.owner_email):
        raise HTTPException(400, "Owner email already exists")

    # Create Business
    bus_data = payload.business.dict()
    bus_data["hashed_password"] = hash_password(bus_data.pop("password"))
    bus_data["owner_id"] = "temp" # Will update after user creation
    
    business_doc = Business(**bus_data).to_dict()
    created_bus = bus_repo.create(business_doc)

    # Create Owner User
    user_data = {
        "name": payload.owner_name,
        "email": payload.owner_email,
        "hashed_password": hash_password(payload.owner_password),
        "role": "owner",
        "business_id": created_bus["id"],
        "is_active": True,
    }
    user_doc = User(**user_data).to_dict()
    created_user = user_repo.create(user_doc)

    # Update Business owner_id
    bus_repo.update(created_bus["id"], {"owner_id": created_user["id"]})

    # Generate token
    token = create_access_token({"business_id": created_bus["id"]})
    
    bus_resp = {k: v for k, v in created_bus.items() if k != "hashed_password"}
    bus_resp["owner_id"] = created_user["id"]
    return {"business_token": token, "business": bus_resp}


@router.post("/business/login")
def login_business(payload: BusinessLoginPayload, db=Depends(get_db)):
    bus_repo = BusinessRepository(db)
    user_repo = UserRepository(db)

    business = bus_repo.get_by_email(payload.email)
    if not business:
        raise HTTPException(404, "Business not found")

    if not verify_password(payload.password, business["hashed_password"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"business_id": business["id"]})
    bus_data = {k: v for k, v in business.items() if k != "hashed_password"}

    # Fetch users for this business
    users = user_repo.get_by_business(business["id"])
    users_data = [{k: v for k, v in u.items() if k != "hashed_password"} for u in users]

    return {"business_token": token, "business": bus_data, "users": users_data}


@router.post("/user/login")
def login_user(email: str, password: str, db=Depends(get_db)):
    user_repo = UserRepository(db)

    user = user_repo.get_by_email(email)
    if not user:
        raise HTTPException(404, "User not found")

    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"user_id": user["id"]})
    user_data = {k: v for k, v in user.items() if k != "hashed_password"}

    return {"access_token": token, "user": user_data}