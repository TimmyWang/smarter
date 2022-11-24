from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base



class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(50))
    customer_id = Column(String(50))
    purchase_time = Column(DateTime)
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_item"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    product_name = Column(String(50))
    product_id = Column(String(50))
    amount = Column(Integer)
    price = Column(Integer)
    order = relationship("Order", back_populates="items")