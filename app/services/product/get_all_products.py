from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.models.product_model import Product

from app.schemas.product.product_response import ProductResponse

def get_all_products(db : Session):
    products = db.query(Product).all()
    if products == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Products were not found")
    return {"products": [ProductResponse.model_validate(product) for product in products]}