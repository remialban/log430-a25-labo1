from daos.product_dao import ProductDAO
from models.product import Product


def test_product_select():
    dao = ProductDAO()
    product_list = dao.select_all()
    assert len(product_list) >= 3

def test_product_insert():
    dao = ProductDAO()
    product = Product(None, 'New Product', 9.99)
    dao.insert(product)
    product_list = dao.select_all()
    names = [p.name for p in product_list]
    assert product.name in names

def test_product_update():
    dao = ProductDAO()
    product = Product(None, 'Updated Product', 19.99)
    dao.insert(product)
    product.price = 29.99
    dao.update(product)
    product_list = dao.select_all()
    assert product.price in [p.price for p in product_list]

def test_product_delete():
    dao = ProductDAO()
    product = Product(None, 'Product to Delete', 9.99)
    dao.insert(product)
    product_list = dao.select_all()
    assert product.name in [p.name for p in product_list]
    dao.delete(product.id)
    product_list = dao.select_all()
    assert product.name not in [p.name for p in product_list]
