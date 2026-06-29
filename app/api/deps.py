from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.database import mongo
from app.core.security import verify_token
from app.repositories.user_repository import UserRepository


# -------------------------------
# SECURITY SCHEME
# -------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


# -------------------------------
# GET DATABASE
# -------------------------------
def get_db():
    return mongo.db


# -------------------------------
# GET CURRENT USER
# -------------------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get("user_id")

    user_repo = UserRepository(mongo.db)
    user = user_repo.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def require_role(allowed_roles: list):
    def role_checker(user: dict = Depends(get_current_user)):
        if user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required roles: {allowed_roles}"
            )
        return user
    return role_checker