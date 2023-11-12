from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    price = Column(Integer)


engine = create_engine("sqlite:///products.db")
Session = sessionmaker()

Base.metadata.create_all(engine)
Session.configure(bind=engine)
session = Session()
session.add(Product(name="cat", category="a", price=11))
session.commit()