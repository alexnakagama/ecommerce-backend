from pydantic import BaseModel

# schema to define the structure of the user registration
class UserRegister(BaseModel):
    username : str
    email : str 
    password : str 