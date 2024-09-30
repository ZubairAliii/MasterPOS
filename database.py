#Database Methods

from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#create all tables from models
engine = create_engine('sqlite:///masterpos.db')
Base.metadata.bind = engine
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()


#login
def DBlogin(username, password):
    user = session.query(User).filter_by(username=username, password=password).first()
    if user:
        return True
    else:
        return False
    

#Get all products
def DBgetproducts():
    products = session.query(Product).all()
    return products

#get category name
def DBgetcategoryname(category_id):
    category = session.query(Category).filter_by(id=category_id).first()
    return category.name

#get all categories
def DBgetcategories():
    categories = session.query(Category).all()
    return categories

#get id of category
def DBgetcategoryid(name):
    category = session.query(Category).filter_by(name=name).first()
    return category.id

#get name of category
def DBgetcategoryname(id):
    category = session.query(Category).filter_by(id=id).first()
    return category.name

#add test users
def DBadduser(username, password, role):
    user = User(username=username, password=password, role=role)
    session.add(user)
    session.commit()


#add product
def DBaddproduct(name, description, barcode, purchase_price, selling_price, quantity, category_id):
    product = Product(name=name, description=description, barcode=barcode, purchase_price=purchase_price, selling_price=selling_price, quantity=quantity, category_id=category_id)
    session.add(product)
    session.commit()
    return True

#update product
def DBupdateproduct(id, name, description, barcode, purchase_price, selling_price, quantity, category_id):
    product = session.query(Product).filter_by(id=id).first()
    product.name = name
    product.description = description
    product.barcode = barcode
    product.purchase_price = purchase_price
    product.selling_price = selling_price
    product.quantity = quantity
    product.category_id = category_id
    session.commit()
    return True


#delete product
def DBdeleteproduct(id):
    product = session.query(Product).filter_by(id=id).first()
    session.delete(product)
    session.commit()
    return True

#load product by category
def DBgetproductsbycategory(category_id):
    products = session.query(Product).filter_by(category_id=category_id).all()
    return products


#get product
def DBgetproduct(id=None,barcode=None):
    if id:
        product = session.query(Product).filter_by(id=id).first()
    elif barcode:
        product = session.query(Product).filter_by(barcode=barcode).first()
    return product



# Add new SAle
def DBaddsale(date, total, barcode,customer_name, customer_number ,user_id,products):
    sale = Sale(date=date, total=total, barcode=barcode, customer_name=customer_name, customer_number=customer_number, user_id=user_id)
    session.add(sale)
    session.commit()
    for p in products.values():
        product = p[0]

        saleproduct = SaleItem(sale_id=sale.id, product_id=product.id, quantity=p[1], price=product.selling_price)
        session.add(saleproduct)
        session.commit()
    return True



#get all sale
def DBgetsale():
    sales = session.query(Sale).all()
    return sales

#get sale and sale item by barcode
def DBgetsalebybarcode(barcode):
    sale = session.query(Sale).filter_by(barcode=barcode).first()
    saleitems = session.query(SaleItem).filter_by(sale_id=sale.id).all()
    return sale,saleitems

# DBadduser('admin', 'admin', 'admin')

# #ADDING TEST DATA FOR PRODUCT AND CATEGORY
# session.add(Category(name='Fast Food'))
# session.add(Category(name='BBQ'))
# session.add(Category(name='Desert'))
# session.add(Category(name='Shakes'))

# session.add(Product(name='Coca Cola', description='Coca Cola', barcode='12345', purchase_price=100, selling_price=150, quantity=10, category_id=1))
# session.add(Product(name='Sprite', description='Sprite', barcode='12346', purchase_price=100, selling_price=150, quantity=10, category_id=1))
# session.add(Product(name='Coke', description='Coke', barcode='12347', purchase_price=100, selling_price=150, quantity=10, category_id=1))
# session.add(Product(name='Fanta', description='Fanta', barcode='12348', purchase_price=100, selling_price=150, quantity=10, category_id=1))
# session.add(Product(name='Lays', description='Lays', barcode='12349', purchase_price=100, selling_price=150, quantity=10, category_id=2))
# session.add(Product(name='Cheetos', description='Cheetos', barcode='12350', purchase_price=100, selling_price=150, quantity=10, category_id=2))
# session.commit()


#get name from product id
def DBgetproductname(id):
    product = session.query(Product).filter_by(id=id).first()
    return product.name

