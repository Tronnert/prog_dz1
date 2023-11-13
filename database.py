from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    date = Column(String)
    price = Column(Integer)


def create_session():
    engine = create_engine("sqlite:///products.db")
    Session = sessionmaker()

    Base.metadata.create_all(engine)
    Session.configure(bind=engine)
    session = Session()
    return session
