from sqlalchemy.orm import Session
from app.models.product_model import Product

# This function creates a new product with the provided name, description, and price.
def create_product(name, description, price, db: Session):
    new_product = Product(name=name, description=description, price=price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product added successfully", "product": new_product}