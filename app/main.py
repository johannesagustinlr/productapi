
from fastapi import FastAPI, Response, status, HTTPException, Request, Depends
from fastapi.params import Body
from datetime import date, datetime, time, timedelta
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


tags_metadata = [
    {
        "name": "products",
        "description": "API for Products CRUD",
    },

    {
        "name": "offers",
        "description": "API for Offers Read",
    },
    
]

description = """
Product API helps you to add product. 🚀

You will be able to:

* **Create products** .
* **Read products** .
* **Update products** .
* **Delete products** .
"""

app = FastAPI(
    title="ProductAPI",
    description=description,
    version="0.0.1",
    openapi_tags = tags_metadata
)
models.Base.metadata.create_all(bind=engine)



#Schema
class Offers(BaseModel):
    availability: str
    price: int
    priceCurrency: str

    class ConfigDict:
        from_attributes = True

class Products(BaseModel):
    name: str
    description: str
    brand: str
    weight: float
    offers: Offers
    image: Optional[str] = None

    class ConfigDict:
        from_attributes = True

class CreatedProducts(Products):
    id: int
    class ConfigDict:
        from_attributes = True

class ProductsUpdate(Products):
    name: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    weight: Optional[float] = None
    offers: Optional[Offers] = None
    image: Optional[str] = None

    class ConfigDict:
        from_attributes = True

    
    



#router


@app.get("/")
def read_root():
    return {"message": "Hello"}


@app.get("/products", tags=["products"])
def get_products(db: Session = Depends (get_db)):
    products = db.query(models.Products).all()
    return {"Data": products}

@app.get("/offers", tags=["offers"])
def get_offers(db: Session = Depends (get_db)):
    offers = db.query(models.Offers).all()
    return {"Data": offers}

@app.get("/offers/{id}",tags=["offers"])
def get_offers(id: int, db: Session = Depends(get_db)):
    offer = db.query(models.Offers).filter(models.Offers.id == id).first()
    if not offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Offer with id = {id} was not found")
    return{"data": offer}

@app.get("/products/{id}",tags=["products"])
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} was not found")
    return{"data": product}

@app.post("/products", status_code=status.HTTP_201_CREATED, tags=["products"])
def create_product(products: Products, db: Session = Depends(get_db)):
    print(products.offers.availability,'testt')
    new_offers = models.Offers(availability = products.offers.availability, price = products.offers.price, priceCurrency = products.offers.priceCurrency)
    db.add(new_offers)
    db.commit()
    db.refresh(new_offers)
    new_products = models.Products(name = products.name, description = products.description, brand = products.brand, weight = products.weight, image = products.image, offer_id=new_offers.id)
    db.add(new_products)
    db.commit()
    db.refresh(new_products)
    return {"data": new_products}

@app.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["products"])
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == id)
    offer = db.query(models.Offers).filter(models.Offers.id == id)
    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} does not exist")
    product.delete(synchronize_session=False)
    if offer.first():
        offer.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.patch("/products/{id}", tags=["products"])
def update_product(id: int, updated_product: ProductsUpdate, db: Session = Depends(get_db),):
    products_query = db.query(models.Products).filter(models.Products.id == id)
    products = products_query.first()

    if products == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"products with id: {id} does not exist")


    update_data = updated_product.dict(exclude_unset=True)
    products_query.update(update_data,synchronize_session=False)
    db.commit()
    db.refresh(products)
    return {"status": "success", "note": products}

    db.commit()




