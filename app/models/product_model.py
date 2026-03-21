from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Integer, nullable=False)