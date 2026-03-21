from fastapi import FastAPI
from app.routers import users
from app.core.database import engine
from app.models.base import Base
from app.models import user_model

# Create the database tables
Base.metadata.create_all(bind=engine)

# Create a FastAPI instance
app = FastAPI()

# Include routers
app.include_router(users.router)