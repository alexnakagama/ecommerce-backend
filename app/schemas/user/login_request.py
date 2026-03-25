from pydantic import BaseModel

# schema to define the structure of the login request on the login endpoint
class LoginRequest(BaseModel):
    username: str
    password: str