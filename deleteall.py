import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///users.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

session.query(User).delete()

session.commit()
