from flask import Flask, render_template, Blueprint

product = Blueprint('products', __name__, url_prefix='/products')

@product.route('/')
def products():
    return render_template("products.html")

@product.route('/bread')
def bread():
    return render_template("bread.html")

@product.route('/checkout')
def checkout():
    return render_template("checkout.html")

@product.route('/drink')
def drink():
    return render_template("drink.html")

@product.route('/frozen')
def frozen():
    return render_template("frozen.html")


@product.route('/pet')
def pet():
    return render_template("pet.html")

@product.route('/vegetables')
def vegetables():
    return render_template("vegetables.html")


@product.route('/single')
def single():
    return render_template("single.html")


@product.route('/payment')
def payment():
    return render_template("payment.html")
