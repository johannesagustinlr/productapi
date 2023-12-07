from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from .database import Base, relationship





class Offers(Base):
    __tablename__ = 'offers'

    id = Column(Integer, primary_key=True, index=True)
    availability = Column(String, nullable = False)
    price = Column(Integer, nullable = False)
    priceCurrency = Column(String, nullable = False)

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable = False)
    description = Column(String, nullable = False)
    brand = Column(String, nullable = False)
    weight = Column(Integer, nullable = False)
    image = Column(String, nullable = True)
    offer_id = Column(Integer, ForeignKey("offers.id"),nullable=False)
    offers = relationship("Offers")
    
