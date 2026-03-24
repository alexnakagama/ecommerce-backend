from sqlalchemy import Column, Integer, ForeignKey
from app.models.base import Base

class CartItems(Base):
    __tablename__ = "cart_items"

    id = Column(Integer ,primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))