from app import db
from app.service.products import ProductService
from app.service.category import CategoryService
from app.view.test import categories, products

product_service = ProductService(db)
cate_service = CategoryService(db)

for k, v in categories.items():
    cate_service.create_category(k, v[0])

for k, v in products.items():
    product_service.create_product(v[0],v[1],v[2],v[3],v[6], v[5],v[4])
