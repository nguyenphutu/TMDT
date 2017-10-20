from flask import Flask, render_template, Blueprint, abort
from app import db
from app.service.products import ProductService
from app.service.category import CategoryService


product = Blueprint('products', __name__, url_prefix='/products')

@product.route('/')
def products():
    cate_survice = CategoryService(db)
    foods = cate_survice.get_product_of_cate(category_name='food')
    vegetables = cate_survice.get_product_of_cate(category_name='vegetables')
    juices = cate_survice.get_product_of_cate(category_name='juices')

    return render_template("products.html", foods=foods, vegetables=vegetables, juices=juices)

@product.route('/<category>')
def product_of_cate(category):
    cate_survice = CategoryService(db)
    products = cate_survice.get_product_of_cate(category_name=category.lower())
    if products:
        category_banner = '_'.join(category.split())
        return render_template("base_product.html", products=products, category_banner=category_banner, category=category)
    abort(404)

@product.route('/<id>/detail')
def product_detail(id):
    product_service = ProductService(db)
    product = product_service.find_product_by_id(product_id=id)
    if product:
        return render_template("single.html", product=product)
    abort(404)

@product.route('/checkout', methods = ['get', 'post'])
def checkout():
    return render_template("checkout.html")

@product.route('/payment')
def payment():
    return render_template("payment.html")
