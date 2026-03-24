from app.core.security import create_access_token, authenticate_user, token_invalidation, get_current_user
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user_model import User
from app.services import create_user as create_user_service
from app.schemas.user.user_create import UserCreate
from app.schemas.user.login_request import LoginRequest

# Create a router for user-related endpoints
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# Endpoint to create a new user
@router.post("/register", summary="Create a new user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service.create_user(user.username, user.email, user.password, user.role, db)

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
async def logout(request: Request):
    token = request.headers.get("authorization")
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]
        token_invalidation(token)
    return {"message": "Successfully logged out"}