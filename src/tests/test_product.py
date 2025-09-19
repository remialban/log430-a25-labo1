from daos.product_dao import ProductDAO
from models.product import Product


def test_product_select():
    dao = ProductDAO()
    product_list = dao.select_all()
    assert len(product_list) >= 3

def test_product_insert():
    dao = ProductDAO()
    product = Product(None, 'New Product', 'BrandX', 9.99)
    assigned_id = dao.insert(product)
    product.id = assigned_id
    product_list = dao.select_all()

    assert len([p for p in product_list if p.id == product.id]) == 1


def test_product_update():
    dao = ProductDAO()
    product = Product(None, 'Updated Product', 'BrandY', 19.99)
    id = dao.insert(product)
    product.id = id
    product.price = 29.99
    dao.update(product)
    product_list = dao.select_all()

    product = [p for p in product_list if p.id == product.id][0]
    print(product.price)
    assert float(product.price) == 29.99

def test_product_delete():
    dao = ProductDAO()
    product = Product(None, 'Product to Delete', 'BrandZ', 9.99)
    id = dao.insert(product)
    product.id = id
    product_list = dao.select_all()
    assert product.name in [p.name for p in product_list]
    dao.delete(product.id)
    product_list = dao.select_all()
    assert product.id not in [p.id for p in product_list]
