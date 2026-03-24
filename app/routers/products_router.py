from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.create_product import create_product as create_product_service

# Create a router for product-related endpoints
router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

# Endpoint to create a new product
@router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_product(name: str, description: str, price: float, db: Session = Depends(get_db)):
    return create_product_service(name, description, price, db)