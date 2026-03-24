from pydantic import BaseModel, Field

# Schema to define the structure of the request body when adding an item to the cart. 
# It includes the product ID and the quantity of the product to be added.
class CartAddItemRequest(BaseModel):
    product_id: int = Field(gt=0, example=1)
    quantity: int = Field(gt=0, example=1)