from flask import Flask, session, render_template, Blueprint, abort, request, make_response, url_for, redirect, flash
from app import db
from app.service.orders import OrderService, OrderDetailService, OrderTempService
from app.service.products import ProductService
# from app.service.report import ReportService
from flask_login import current_user
# order_service = OrderService(db)
# order_detail_service = OrderDetailService(db)
order_temp_service = OrderTempService(db)
order_service = OrderService(db)
product_service = ProductService(db)
# report_service = ReportService()

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
        if current_user.is_authenticated:
            order = order_temp_service.find_order_by_product_id(current_user.id, product_id)
            if order:
                order_temp_service.update(order, quantity)
            else:
                user_id = int(current_user.id)
                price = product.price - round((product.price*product.sale)/100, 2)
                order = order_temp_service.create_order_temp(user_id=user_id, product_id=product_id, quantity=quantity, price=price)
            if order:
                flash(u'Add product to cart successfully', 'success')
        else:
            if 'orders_temps' not in session:
                session['orders_temps'] = {}
                session['orders_temps'][str(product_id)] = quantity
            else:
                session['orders_temps'][str(product_id)] = quantity
                print(session['orders_temps'])
        return redirect(url_for('products.checkout'))
@order.route('/delete/<id>', methods = ['POST'])
def delete(id):
    if id:
        if current_user.is_authenticated:
            order = order_temp_service.delete_order_temp_by_id(id)
            if order:
                flash(u'Delete product successfully', 'success')
        else:
            del session['orders_temps'][id]
            print(session['orders_temps'])
        return redirect(url_for('products.checkout'))
    abort(404)

@order.route('/save_change/<id>', methods = ['POST'])
def save_change(id):
    if id:
        quality = request.form['quality']
        if current_user.is_authenticated:
            order = order_temp_service.update(id, quantity=quality)
            if order:
                flash(u'update product successfully', 'success')
            else:
                flash(u'update product error', 'warring')
        elif id in session['orders_temps']:
            session['orders_temps'][id] = quality
            flash(u'update product successfully', 'success')
        return redirect(url_for('products.checkout'))
    abort(404)

@order.route("/download_invoice/<id>")
def download_invoice(id):
    if id:
        order = order_service.find_order_by_id(id)
        if order:
            order_details = order.order_details
            user_detail = current_user.user_detail
            pdf = report_service.to_pdf(context={
                'user_detail': user_detail,
                'order_date': order.date_created.strftime("%b %d %Y"),
                'order_details': order.order_details})
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
            return response
    else:
        abort(404)
