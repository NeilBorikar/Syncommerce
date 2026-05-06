from fastapi import APIRouter, Depends
from app.api.deps import get_db, get_current_user
from app.repositories.user_repository import UserRepository

router = APIRouter()


@router.get("/me")
def get_me(user=Depends(get_current_user)):
    return user


@router.get("/business/{business_id}")
def get_users(business_id: str, db=Depends(get_db)):
    repo = UserRepository(db)
    return repo.get_by_business(business_id)