from app.model.product import Product
from app.model.category import Category
import uuid

class ProductService():
    def __init__(self, db):
        self.db = db

    def all(self):
        return Product.query.all()

    def create_product(self, name, info, quantity, price, category_id, sale=None):
        category = Category.query.filter_by(id=category_id).first()
        product = Product()
        product.name = name
        product.info = info
        product.quantity = quantity
        product.price = price
        product.sale = sale
        product.slug = str(uuid.uuid4())
        product.category_id = category_id
        product.category = category
        try:
            self.db.session.add(product)
            self.db.session.commit()
            return product
        except Exception as e:
            self.db.session.rollback()
            return None

    def change_product(self, product_id, name, info, quantity, price, category_id, sale=None):
        product = Product.query.filter_by(id=product_id).first()
        if product:
            category = Category.query.filter_by(id=category_id).first()
            product.name = name
            product.info = info
            product.quantity = product.quantity + int(quantity)
            product.price = price
            product.sale = sale
            product.category_id = category_id
            product.category = category
            self.db.session.commit()
            return product
        else:
            return None

    def add_product_sale(self, product_id, sale):
        product = Product.query.filter_by(id=product_id).first()
        if product:
            product.sale = sale
            self.db.commit(f'update sale for product {product.name}')
            return product
        else:
            return "Error ,no product"

    def add_category_product_sale(self, category_id, sale):
        products = Product.query.filter_by(category_id=category_id)
        if products:
            for product in products:
                product.sale = sale
                self.db.commit()
            return products
        else:
            return "Error ,no category"

    def find_product_by_id(self, product_id):
        product = Product.query.filter_by(id=product_id).first()
        if product:
            return product
        else:
            return None

    def delete(self, id):
        product = Product.query.filter_by(id=id).first()
        if product:
            self.db.session.delete(product)
            self.db.session.commit()
            return product
        return None

    def get_product_sale(self):
        product = Product.query.filter(Product.sale > 0).order_by(Product.sale.desc())
        return product

