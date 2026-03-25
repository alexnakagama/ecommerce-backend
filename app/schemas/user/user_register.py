from pydantic import BaseModel, Field

class UserRegister(BaseModel):
    username : str = Field(examples="fran123")
    email : str = Field(examples="fran@gmail.com")
    password : str = Field(examples="test123")