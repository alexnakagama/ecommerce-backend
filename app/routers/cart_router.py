from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.user_model import User
from app.models.product_model import Product
from app.models.cart_model import Cart
from app.models.cart_items import CartItems

from app.schemas.cart.cart_add_item_request import CartAddItemRequest
from app.schemas.product.product_response import ProductResponse

from app.services.user.get_user_cart import get_user_cart

# Create a router for cart-related endpoints
router = APIRouter(
    prefix="/cart",
    tags=["cart"],
    responses={404: {"description": "Not found"}},
)

# Endpoint to get the current users cart
@router.get("", summary="Get current users cart")
async def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_cart(db, current_user)

# Endpoint to add an item to the cart. It expects a request body that matches the CartAddItemRequest schema.
@router.post("/add", summary="Add item to cart")
async def add_to_cart(request: CartAddItemRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Placeholder for adding an item to the cart
    return {"message": "Add item to cart"}

# Endpoint to remove an item from the cart. 
# It can be implemented to accept necessary parameters to identify the item to be removed.
@router.post("/remove", summary="Remove item from cart")
async def remove_from_cart(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Placeholder for removing an item from the cart
    return {"message": "Remove item from cart"}

# Endpoint to clear the cart. It will remove all items from the user's cart.
@router.post("/clear", summary="Clear cart")
async def clear_cart(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Placeholder for clearing the cart
    return {"message": "Clear cart"}

# Endpoint to update the quantity of an item in the cart. 
@router.put("/update", summary="Update item quantity in cart")
async def update_cart(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Placeholder for updating item quantity in the cart
    return {"message": "Update item quantity in cart"}
