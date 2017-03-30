import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from products import *

engine = create_engine('sqlite:///products.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

session.query(Products).delete()

session.commit()
