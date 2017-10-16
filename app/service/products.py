from app.model.product import Product

class ProductService():
    def __init__(self, db):
        self.db = db

    def all(self):
        return Product.query.all()

    def create_product(self, name, info, so_luong, gia_ban, slug, category_id, category, sale=None):
        product = Product()
        product.name = name
        product.info = info
        product.so_luong = so_luong
        product.gia_ban = gia_ban
        product.sale = sale
        product.slug = slug
        product.category_id = category_id
        product.category = category

        status = ''
        try:
            self.db.add(product)
            self.db.commit('Add new product')
        except Exception as e:
            status = "Add product error"

        if status != '':
            return status
        return product

    def change_product(self, product_id, name, info, so_luong, gia_ban, slug, category_id, category, sale=None):
        product = Product.query.filter_by(id=product_id).first()
        if product:
            product.name = name
            product.info = info
            product.so_luong = so_luong
            product.gia_ban = gia_ban
            product.sale = sale
            product.slug = slug
            product.category_id = category_id
            product.category = category
            self.db.commit(f'update product {product.name}')
            return product
        else:
            return "Error ,no product"

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
