from pydantic import BaseModel, EmailStr

# This schema is used to define the structure of the response when a user is created or retrieved. 
# It includes all the fields that are expected in the response.
class UserResponse(BaseModel):
    email: EmailStr
    username: str

    # This allows the model to be created from ORM objects
    class Config:
        from_attributes = True