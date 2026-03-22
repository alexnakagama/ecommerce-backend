from fastapi import FastAPI
from app.routers import admin, products, users
from app.core.database import engine
from app.models.base import Base

# Create the database tables
Base.metadata.create_all(bind=engine)

# Create a FastAPI instance
app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(admin.router)
