from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.services.create_product import create_product as create_product_service

from app.models.user_model import User

# Create a router for product-related endpoints
router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

# Endpoint to do a petition 
@router.post("", summary="Create a request for a product",status_code=status.HTTP_201_CREATED)
async def create_request_product():
    pass