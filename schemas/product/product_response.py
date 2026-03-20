from pydantic import BaseModel

# This schema is used to define the structure of the response when a product is created or retrieved. 
# It includes all the fields that are expected in the response.
class ProductResponse(BaseModel):
    name: str
    description: str
    price: float
    stock: int

    # This allows the model to be created from ORM objects
    class Config:
        from_attributes = True