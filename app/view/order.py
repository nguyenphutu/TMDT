from flask import Flask, render_template, Blueprint, abort, request, jsonify, url_for, redirect, flash
from app import db
from app.service.orders import OrderService, OrderDetailService, OrderTempService
from app.service.products import ProductService
from flask_login import current_user
# order_service = OrderService(db)
# order_detail_service = OrderDetailService(db)
order_temp_service = OrderTempService(db)
product_service = ProductService(db)

order = Blueprint('order', __name__, url_prefix='/orders')

@order.route('/create', methods = ['POST'])
def create_order():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        if 'quantity' in request.form:
            quantity = request.form['quantity']
        else:
            quantity = 1
        product = product_service.find_product_by_id(product_id)
        order = order_temp_service.find_order_by_product_id(product_id)
        if order:
            order_temp_service.update(order, quantity)
        else:
            user_id = int(current_user.id)
            price = product.price - round((product.price*product.sale)/100, 2)
            order = order_temp_service.create_order_temp(user_id=user_id, product_id=product_id, quantity=quantity, price=price)
        if order:
            flash(u'Add product to cart successfully', 'success')
        return redirect(url_for('products.checkout'))

@order.route('/delete/<id>', methods = ['POST'])
def delete(id):
    if id:
        order = order_temp_service.delete_order_temp_by_id(id)
        if order:
            flash(u'Delete product successfully', 'success')
        return redirect(url_for('products.checkout'))
    abort(404)

@order.route('/save_change/<id>', methods = ['POST'])
def save_change(id):
    if id:
        quality = request.form['quality']
        order = order_temp_service.update(id, quantity=quality)
        if order:
            flash(u'update product successfully', 'success')
        return redirect(url_for('products.checkout'))
    abort(404)