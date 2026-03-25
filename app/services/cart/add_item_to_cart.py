from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.models.cart_model import Cart
from app.models.product_model import Product
from app.models.cart_items import CartItems
from app.models.user_model import User

from app.schemas.cart.cart_add_item_request import CartAddItemRequest


def add_item_to_cart(db : Session, user : User, request : CartAddItemRequest):
    product = db.query(Product).filter(Product.id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active cart found")
    cart = db.query(Cart).filter(Cart.user_id == user.id, Cart.is_active == True).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active cart found")
    cart_item = db.query(CartItems).filter(CartItems.cart_id == cart.id,CartItems.product_id == request.product_id).first()
    if cart_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item already in cart")
    new_item = CartItems(cart_id=cart.id, product_id=request.product_id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item