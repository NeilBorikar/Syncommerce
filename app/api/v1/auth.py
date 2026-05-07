from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schema import UserCreate
from app.services.billing_service import BillingService
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.api.deps import get_db


router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db=Depends(get_db)):
    repo = UserRepository(db)

    existing = repo.get_by_email(user.email)
    if existing:
        raise HTTPException(400, "Email already exists")

    user_data = user.dict()
    user_data["hashed_password"] = hash_password(user_data.pop("password"))

    return repo.create(user_data)


@router.post("/login")
def login(email: str, password: str, db=Depends(get_db)):
    repo = UserRepository(db)

    user = repo.get_by_email(email)
    if not user:
        raise HTTPException(404, "User not found")

    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"user_id": user["id"]})

    user_data = {k: v for k, v in user.items() if k != "hashed_password"}

    return {"access_token": token, "user": user_data}