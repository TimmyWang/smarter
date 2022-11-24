from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base



class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(50), nullable=False)
    customer_id = Column(String(50), nullable=False)
    purchase_time = Column(DateTime, nullable=False)
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_item"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    product_name = Column(String(50), nullable=False)
    product_id = Column(String(50), nullable=False)
    amount = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    order = relationship("Order", back_populates="items")