from pydantic import BaseModel

# schema to define the structure of the product request body when requesting for a product
class ProductRequest(BaseModel):
    name : str
    quantity : int