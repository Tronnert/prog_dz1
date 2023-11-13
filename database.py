from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.sql import func
import datetime
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    date = Column(DateTime(), default=datetime.datetime.now)
    price = Column(Integer)


def create_session():
    engine = create_engine("sqlite:///products.db")
    Session = sessionmaker()

    Base.metadata.create_all(engine)
    Session.configure(bind=engine)
    session = Session()
    return session
