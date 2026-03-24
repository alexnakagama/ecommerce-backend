from sqlalchemy import Column, Integer, Boolean, ForeignKey
from app.models.base import Base

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean)