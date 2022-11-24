from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from db import models
from db.database import engine, SessionLocal
from sqlalchemy.orm import Session



app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
	try:
		db = SessionLocal()
		yield db
	finally:
		db.close()


class OrderItem(BaseModel):
	product_name: str = Field(min_length=1, max_length=100)
	product_id: str = Field(min_length=1, max_length=100)
	amount: int = Field(gt=0)
	price: int = Field(gt=0)
	id: Optional[int] = None
	delete: Optional[bool] = False


class Order(BaseModel):
	customer_name: str = Field(min_length=1)
	customer_id: str = Field(min_length=1, max_length=100)
	items: list[OrderItem]


class Update:

	def order(order_model, order, date=True):
		order_model.customer_name = order.customer_name
		order_model.customer_id = order.customer_id
		if date:
			order_model.purchase_time = datetime.now()

	def item(item_model, item, order_id):
		item_model.order_id = order_id
		item_model.product_name = item.product_name
		item_model.product_id = item.product_id
		item_model.amount = item.amount
		item_model.price = item.price


@app.get("/order/{order_id}")
def get_order(order_id:int, db: Session = Depends(get_db)):
	
	order_model = db.query(models.Order).filter(models.Order.id == order_id).first()
	
	if not order_model:
		raise HTTPException(
			status_code=404,
			detail=f"Order id {order_id} does not exist"
		)
	
	order_model.items = order_model.items

	return order_model


@app.post("/order/add")
def add_order(order: Order, db: Session = Depends(get_db)):

	order_model = models.Order()
	Update.order(order_model, order)
	db.add(order_model)
	db.commit()

	order_id = order_model.id
	for item in order.items:
		item_model = models.OrderItem()
		Update.item(item_model, item, order_id)
		db.add(item_model)

	db.commit()

	return {"order_id":order_id}


@app.put("/order/modify/{order_id}")
def modify_order(order_id:int, order: Order, db: Session = Depends(get_db)):

	order_model = db.query(models.Order).filter(models.Order.id == order_id).first()

	if not order_model:
		raise HTTPException(
			status_code=404,
			detail=f"Order id {order_id} does not exist"
		)

	Update.order(order_model, order, date=False)

	item_ids = [item.id for item in order_model.items]

	for item in order.items:
		if item.id is None:
			item_model = models.OrderItem()
			Update.item(item_model, item, order_id)
			db.add(item_model)
		elif item.id in item_ids:
			item_model = db.query(models.OrderItem).filter(models.OrderItem.id == item.id).first()
			if item.delete:
				db.delete(item_model)
			else:
				Update.item(item_model, item, order_id)
		else:
			raise HTTPException(
				status_code=404,
				detail=f"Item id {item.id} does not exist"
			)

	db.commit()

	return order

