from fastapi import FastAPI
from app.routers import products, users
from app.core.database import engine
from app.models.base import Base
from app.models import user_model

# Create the database tables
Base.metadata.create_all(bind=engine)

# Create a FastAPI instance
app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(products.router)