from fastapi import FastAPI

from app.routers import admin_router, cart_router, products_router, users_router

from app.core.database import engine

from app.models.base import Base
from app.models.cart_model import Cart
from app.models.cart_items import CartItems

# Create the database tables
Base.metadata.create_all(bind=engine)

# Create a FastAPI instance
app = FastAPI()

# Include routers
app.include_router(users_router.router)
app.include_router(products_router.router)
app.include_router(admin_router.router)
app.include_router(cart_router.router)
