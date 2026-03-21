from pydantic import BaseModel, EmailStr,Field

# This schema is used to define the structure of the request body when creating a new user.
class UserCreate(BaseModel):
    username: str = Field(max_length=20, min_length=5, example="john_doe")
    email: EmailStr = Field(max_length=30, example="john_doe@example.com")
    password: str = Field(min_length=6, max_length=20, example="strong_password")
    role: str = Field(default="customer", example="customer")