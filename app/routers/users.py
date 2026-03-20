from fastapi import APIRouter, status
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
async def create_user(user: UserCreate):
    return create_user_service.create_user(user.username, user.email, user.password)