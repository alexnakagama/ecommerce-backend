from fastapi import FastAPI
from app.routers import users

# Create a FastAPI instance
app = FastAPI()

# Include routers
app.include_router(users.router)