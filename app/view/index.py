from flask import Flask, render_template, Blueprint, request, jsonify
from app import db
from app.service.products import ProductService
from app.service.category import CategoryService

web = Blueprint('web', __name__, url_prefix='/')
product_service = ProductService(db)
cate_service = CategoryService(db)

@web.route('/')
def homepage():
    hotOffers = product_service.get_product_sale()
    return render_template("index.html", hotOffers=hotOffers)

def test_data():
    products = product_service.all()
    cates = cate_service.all()
    products_list = {}
    for pro in products:
        list_pro = [pro.name, pro.info, pro.quantity, pro.price, pro.sale, pro.slug, pro.category_id]
        products_list[pro.id] = list_pro

    cates_list = {}
    for cate in cates:
        list_cate = [cate.name, cate.url]
        cates_list[cate.id] = list_cate

    print(cates_list)
    print(products_list)
    return jsonify(products_list=products_list, cates_list=cates_list)
