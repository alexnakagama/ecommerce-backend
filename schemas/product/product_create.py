from pydantic import BaseModel, Field

# This schema is used to define the structure of the request body when creating a new product.
class ProductCreate(BaseModel):
    name: str = Field(max_length=50, min_length=3, example="Laptop")
    description: str = Field(max_length=100, min_length=10, example="A high-performance laptop for gaming and work.")
    price: float = Field(gt=0, example=999.99)
    stock: int = Field(ge=0, example=10)