from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import create_user as create_user_service
from app.schemas.user.user_create import UserCreate

# Create a router for user-related endpoints
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# Endpoint to create a new user
@router.post("/create-user", summary="Create a new user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service.create_user(user.username, user.email, user.password, user.role, db)