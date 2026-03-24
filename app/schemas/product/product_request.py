from pydantic import BaseModel

class ProductRequest(BaseModel):
    name : str
    quantity : int