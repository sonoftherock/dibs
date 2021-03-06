from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()

########################################################################
class User(Base):
    """"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    venmoacc = Column(String)
    entrance = Column(Integer, default=0)
    bid = Column(Float, default=0.0)

    #----------------------------------------------------------------------
    def __init__(self, username, password, venmoacc):
        """"""
        self.username = username
        self.password = password
        self.venmoacc = venmoacc
# create tables
Base.metadata.create_all(engine)
