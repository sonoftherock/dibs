import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from products import *

engine = create_engine('sqlite:///products.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

products = Products("https://sneakerbardetroit.com/wp-content/uploads/2016/09/adidas-yeezy-350-boost-v2-beluga-grey-solar-red-1.jpg","Yeezy Boost",2.0, 500, 0)
session.add(products)

# commit the record the database
session.commit()
