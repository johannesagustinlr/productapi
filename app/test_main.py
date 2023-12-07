from fastapi.testclient import TestClient
from fastapi import status
import pytest
from .main import app, Products
from .config import DATABASE_UNAME, DATABASE_PASS, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base


SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_UNAME}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

client = TestClient(app=app)


def test_index():
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello"}


def test_get_all_products():
    response = client.get("/products")
    assert response.status_code == status.HTTP_200_OK


    
def test_create_product():
    product_data = {
            "@context": "https://schema.org",
            "@type": "Product",
            "id": 1,
            "name": "Kenmore White 17\" Microwave",
            "description": "7 cubic feet countertop microwave. Has six preset cooking categories and convenience features like Add-A-Minute and Child Lock.",
            "brand": "Kenmore",
            "offers": {
                "@type": "Offer",
                "availability": "https://schema.org/InStock",
                "price": "55.00",
                "priceCurrency": "USD"
            },
            "weight": 250,
            "image": "kenmore-microwave-17in.jpg"
        }
    


    response = client.post("/products", json=product_data)
    
    assert response.status_code == status.HTTP_201_CREATED
