import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from products import *

engine = create_engine('sqlite:///products.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

products = Products("http://www.pacificsandiego.com/wp-content/uploads/2016/01/omnia1-2-1.jpg","Chainsmokers Ticket",2.0, 140, 0)
session.add(products)

# commit the record the database
session.commit()
