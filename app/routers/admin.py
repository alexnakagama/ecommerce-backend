from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_model import User
from app.routers.users import router as users_router
from app.routers.products import router as products_router

# Create a router for admin-related endpoints
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

# Endpoint to get admin dashboard information
@router.get("/dashboard", summary="Get admin dashboard information", status_code=status.HTTP_200_OK)
async def get_admin_dashboard(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return {"message": f"Welcome to the admin dashboard, {current_user['username']}!"}

# Endpoint to manage users (example: list all users)
@router.get("/users", summary="List all users", status_code=status.HTTP_200_OK)
async def list_users(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    users = db.query(User).all()
    return {"users": users}

# Endpoint to get user by ID
@router.get("/users/{user_id}", summary="Get user by ID", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"user": user}

# Endpoint to delete a user by ID
@router.delete("/users/{user_id}", summary="Delete user by ID", status_code=status.HTTP_200_OK)
async def delete_user_by_id(user_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    db.refresh(user)
    return {"message": "User deleted successfully"}