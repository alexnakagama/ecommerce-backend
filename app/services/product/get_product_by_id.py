from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.models.product_model import Product

from app.schemas.product.product_response import ProductResponse

def get_product_by_id(db : Session, product_id : int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product was not found")
    return ProductResponse.model_validate(product)