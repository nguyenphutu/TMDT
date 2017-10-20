from flask import Flask, render_template, Blueprint
from app import db
from app.service.products import ProductService

web = Blueprint('web', __name__, url_prefix='/')

@web.route('/')
def homepage():
    product_service = ProductService(db)
    hotOffers = product_service.get_product_sale()
    return render_template("index.html", hotOffers=hotOffers)

