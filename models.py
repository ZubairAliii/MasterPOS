from sqlalchemy import Column, Integer, String , DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

#Product
class Product(Base):
    __tablename__ = 'products'
    #autoincrement id
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    barcode = Column(String)
    purchase_price = Column(Integer)
    selling_price = Column(Integer)
    quantity = Column(Integer)
    category_id = Column(Integer)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)

#Sale and Sale Item
class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    customer_name = Column(String)
    customer_number = Column(String)
    total = Column(Integer)
    barcode = Column(String)
    user_id = Column(Integer) #user id

class SaleItem(Base):
    __tablename__ = 'sale_items'
    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)
    price = Column(Integer)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    role = Column(String)

