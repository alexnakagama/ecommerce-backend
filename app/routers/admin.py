from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import check_admin
from app.models.user_model import User
from app.services.create_product import create_product as create_product_service
from app.schemas.product.product_create import ProductCreate
from app.schemas.user.user_response import UserResponse
from app.schemas.product.product_response import ProductResponse
from app.models.product_model import Product

# Create a router for admin-related endpoints
router = APIRouter(
    prefix="/admin/dashboard",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

# Endpoint to get admin dashboard information
@router.get("", summary="Get admin dashboard information", status_code=status.HTTP_200_OK)
async def get_admin_dashboard(current_user: dict = Depends(check_admin), db: Session = Depends(get_db)):
    return {"message": f"Welcome to the admin dashboard, {current_user['username']}!"}

# Endpoint to manage users (example: list all users)
@router.get("/users", summary="List all users", status_code=status.HTTP_200_OK)
async def list_users(current_user: dict = Depends(check_admin), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": [UserResponse.model_validate(user) for user in users]}

# Endpoint to get user by ID
@router.get("/users/{user_id}", summary="Get user by ID", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, current_user: dict = Depends(check_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"user": UserResponse.model_validate(user)}

# Endpoint to delete a user by ID
@router.delete("/users/{user_id}", summary="Delete user by ID", status_code=status.HTTP_200_OK)
async def delete_user_by_id(user_id: int, current_user: dict = Depends(check_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    db.refresh(user)
    return {"message": "User deleted successfully"}

# Endpoint to update user role (example: promote a user to admin)
@router.put("/users/{user_id}/role", summary="Update user role", status_code=status.HTTP_200_OK)
async def update_user_role(user_id: int, new_role: str, current_user: dict = Depends(check_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.role = new_role
    db.commit()
    db.refresh(user)
    return {"message": f"User role updated to {new_role} successfully"}

# Endpoint to create a new product (example: add a new product to the inventory)
@router.post("/products/add", summary="Create a new product", status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate, current_user: dict = Depends(check_admin), db: Session = Depends(get_db)):
    name = product_data.name
    description = product_data.description
    price = product_data.price
    if not name or not description or price is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing product data")
    return create_product_service(name, description, price, db)

# Endpoint to list all products
@router.get("/products", summary="List all products", status_code=status.HTTP_200_OK)
async def list_products(current_user: dict = Depends(check_admin), db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return {"products": [ProductResponse.model_validate(product) for product in products]}

# Endpoint to list a product by ID
@router.get("/products/{product_id}", summary="List a product by ID", status_code=status.HTTP_200_OK)
async def list_product_by_id(product_id: int, current_user: dict = Depends(check_admin), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product was not found")
    return ProductResponse.model_validate(product)