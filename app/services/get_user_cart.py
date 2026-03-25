from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.models.user_model import User
from app.models.cart_model import Cart
from app.models.cart_items import CartItems
from app.models.product_model import Product

from app.schemas.product.product_response import ProductResponse

def get_user_cart(db: Session, user: User):
    product_list = []
    db_cart = db.query(Cart).filter(Cart.user_id == user.id, Cart.is_active == True).first()
    if not db_cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This cart doesnt exist or is inactive")
    cart_items = db.query(CartItems).filter(CartItems.cart_id == db_cart.id).all()
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product_list.append(ProductResponse.model_validate(product))
    return product_list