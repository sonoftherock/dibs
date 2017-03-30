from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///products.db', echo=True)
Base = declarative_base()

########################################################################
class Products(Base):
    """"""
    __tablename__ = "products"

    product_image = Column(String)
    product_name = Column(String, primary_key=True)
    entry_fee = Column(Float)
    retail_price = Column(Integer)
    bidders = Column(Integer)

    #----------------------------------------------------------------------
    def __init__(self,product_image, product_name, entry_fee, retail_price, bidders):
        """"""
        self.product_image = product_image
        self.product_name = product_name
        self.entry_fee = entry_fee
        self.retail_price = retail_price
        self.bidders = bidders
# create tables
Base.metadata.create_all(engine)
