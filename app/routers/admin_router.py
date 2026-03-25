# enviroment imports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# core imports
from app.core.database import get_db
from app.core.security import check_admin

# model imports
from app.models.user_model import User
from app.models.product_model import Product

# services imports
from app.services.product.create_product import create_product as create_product_service
from app.services.admin.create_user_admin import create_user_admin as create_user_admin_service
from app.services.admin.get_user_by_id import get_user_by_id as get_user_id
from app.services.admin.delete_user_by_id import delete_user_by_id as delete_user_id
from app.services.admin.update_user_role import update_user_role as update_user_role_service
from app.services.product.get_product_by_id import get_product_by_id
from app.services.product.get_all_products import get_all_products

# schemas imports
from app.schemas.product.product_create import ProductCreate
from app.schemas.user.user_create import UserCreate
from app.schemas.user.user_response import UserResponse
from app.schemas.product.product_response import ProductResponse


# Create a router for admin-related endpoints
router = APIRouter(
    prefix="/admin/dashboard",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

# Endpoint to get admin dashboard information
@router.get("", summary="Get admin dashboard information", status_code=status.HTTP_200_OK)
async def get_admin_dashboard(current_user: dict = Depends(check_admin), db: Session = Depends(get_db)):
    return {"message": f"Welcome to the admin dashboard, {current_user.username}!"}

# Endpoint to create a user
@router.post("/users/create", summary="Create a user", status_code=status.HTTP_201_CREATED)
async def create_user_admin(user_data: UserCreate, current_user: User = Depends(check_admin), db: Session = Depends(get_db)):
    return create_user_admin_service(db, user_data)

# Endpoint to manage users (example: list all users)
@router.get("/users", summary="List all users", status_code=status.HTTP_200_OK)
async def list_users(current_user: User = Depends(check_admin), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": [UserResponse.model_validate(user) for user in users]}

# Endpoint to get user by ID
@router.get("/users/{user_id}", summary="Get user by ID", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, current_user: User = Depends(check_admin), db: Session = Depends(get_db)):
    return get_user_id(db, user_id)

# Endpoint to delete a user by ID
@router.delete("/users/delete/{user_id}", summary="Delete user by ID", status_code=status.HTTP_200_OK)
async def delete_user_by_id(user_id: int, current_user: User = Depends(check_admin), db: Session = Depends(get_db)):
    return delete_user_id(db, user_id)

# Endpoint to update user role (example: promote a user to admin)
@router.put("/users/{user_id}/role", summary="Update user role", status_code=status.HTTP_200_OK)
async def update_user_role(user_id: int, new_role: str, current_user: User = Depends(check_admin), db: Session = Depends(get_db)):
    return update_user_role_service(db, user_id, new_role)

# Endpoint to create a new product (example: add a new product to the inventory)
@router.post("/products/add", summary="Create a new product", status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate, current_user: User = Depends(check_admin), db: Session = Depends(get_db)):
    name = product_data.name
    description = product_data.description
    price = product_data.price
    if not name or not description or price is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing product data")
    return create_product_service(name, description, price, db)

# Endpoint to list all products
@router.get("/products", summary="List all products", status_code=status.HTTP_200_OK)
async def list_products(current_user: User = Depends(check_admin), db: Session = Depends(get_db)):
    return get_all_products(db)

# Endpoint to list a product by ID
@router.get("/products/{product_id}", summary="List a product by ID", status_code=status.HTTP_200_OK)
async def list_product_by_id(product_id: int, current_user: User = Depends(check_admin), db: Session = Depends(get_db)):
    return get_product_by_id(db, product_id)

