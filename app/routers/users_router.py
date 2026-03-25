from app.core.security import create_access_token, authenticate_user, token_invalidation, get_current_user

from fastapi import APIRouter, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.user_model import User

from app.services.create_user import create_user as create_user_service
from app.services.update_user import update_user_info

from app.schemas.user.user_create import UserCreate
from app.schemas.user.user_modify import UserModify

# Create a router for user-related endpoints
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# Endpoint to create a new user
@router.post("/register", summary="Create a new user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(user.username, user.email, user.password, user.role, db)

# Endpoint for user login
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }
    return {"access_token": create_access_token(user_data), "token_type": "bearer"}

# Endpoint to get the current user's information
@router.get("/me", summary="Get current user's information")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Endpoint to logout
@router.post("/logout")
async def logout(request: Request, current_user: User = Depends(get_current_user)):
    token = request.headers.get("authorization")
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]
        token_invalidation(token)
    return {"message": "Successfully logged out"}

# Endpoint to modify my user information
@router.put("/me/modify", summary="Modify current user's information")
async def update_user(user: UserModify, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_user_info(db, current_user.id, user.username, user.email)

# Endpoint to change my password
@router.put("/me/password", summary="Change current user's password")
async def change_password(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if db_user:
        db_user.password_hash = user.password
        db.commit()
        return {"message": "Password changed successfully"}
    return {"message": "User not found"}

# Endpoint to delete my account
@router.delete("/me/delete", summary="Delete current user's account")
async def delete_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "User account deleted successfully"}
    return {"message": "User not found"}