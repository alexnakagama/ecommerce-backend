from pydantic import BaseModel

# schema to define the structure for the password change request
class ChangePasswordRequest(BaseModel):
    old_password : str
    new_password : str