from flask import session, render_template, Blueprint, abort, request, make_response, url_for, redirect
from flask_login import current_user, login_required
from app import db
from app.service.products import ProductService
from app.service.category import CategoryService
from app.service.orders import OrderTempService, OrderDetailService, OrderService
from app.service.user import UserDetailService
from app.form import CheckoutForm
from app.utils import send_mail

product = Blueprint('products', __name__, url_prefix='/products')
order_temp_service = OrderTempService(db)
order_detail_service = OrderDetailService(db)
order_service = OrderService(db)
product_service = ProductService(db)
cate_survice = CategoryService(db)
user_detail_service = UserDetailService(db)

@product.route('/', methods=['GET'])
def products():
    foods = cate_survice.get_product_of_cate(category_name='food')
    vegetables = cate_survice.get_product_of_cate(category_name='vegetables')
    juices = cate_survice.get_product_of_cate(category_name='juices')
    if request.args.get('search'):
        search = request.args.get('search')
        pros = product_service.search(search)
        return render_template("base_product.html", products=pros)
    return render_template("products.html", foods=foods, vegetables=vegetables, juices=juices)

@product.route('/<category>')
def product_of_cate(category):
    products = cate_survice.get_product_of_cate(category_name=category.lower())
    if products:
        category_banner = '_'.join(category.split())
        return render_template("base_product.html", products=products, category_banner=category_banner, category=category)
    abort(404)

@product.route('/<id>/detail')
def product_detail(id):
    product = product_service.find_product_by_id(product_id=id)
    if product:
        return render_template("single.html", product=product)
    abort(404)

@product.route('/checkout', methods = ['get', 'post'])
def checkout():
    form = CheckoutForm(request.form)
    # order_temps = order_temp_service.all(user.id)
    if current_user.is_authenticated:
        order_temps = current_user.order_temps
    else:
        try:
            order_temps = render_order_from_session(session['orders_temps'])
        except Exception as e:
            order_temps = []
    if request.method == 'POST' and form.validate():
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        fullname = request.form['fullname']
        city = request.form['city']
        district = request.form['district']
        ward = request.form['ward']
        phone = request.form['phone']
        address = request.form['address']
        if not current_user.user_detail:
            user_detail = user_detail_service.create_user_detail(
                fullname=fullname,
                city=city,
                district=district,
                ward=ward,
                address=address,
                phone=phone,
                user_id=current_user.id
            )
        else:
            user_detail = user_detail_service.update_user_detail(
                fullname=fullname,
                city=city,
                district=district,
                ward=ward,
                address=address,
                phone=phone,
                user_id=current_user.id
            )
        if len(order_temps) != 0:
            order = order_service.create_order(user_id=current_user.id)
            total_pay = 0
            for temp in order_temps:
                order_detail = order_detail_service.create_order_detail(
                    order_id=order.id,
                    product_id=temp.product_id,
                    quantity=temp.quantity,
                    price=temp.price,
                )
                if order_detail:
                    total_pay += order_detail.quantity*order_detail.price
            order.total_payment = total_pay
            order_temp_service.delete_order_temps()
                # send_mail.send_invoice_email(order.id, user.email)
            return render_template("view_order.html", order_date=order.date_created.strftime("%b %d %Y"), order_details=order.order_details)
        else:
            return render_template("checkout.html", orders=order_temps)
    return render_template("checkout.html", orders=order_temps)

@product.route('/payment')
def payment():
    return render_template("payment.html")

@product.route('/dowload_order_detail')
def dowload_pdf():
    import pdfkit
    path_wkthmltopdf = r'F:\Progrram Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    path = url_for('static', filename='pdf')+'/aaa.pdf'
    print(path)
    pdf = pdfkit.from_string(render_template("test.html"), configuration=config, output_path=path)
    response = make_response(pdf)
    response.headers['Content-Type'] = "application/pdf"
    response.headers['Content-Disposition'] = "attachment; filename='test.pdf"
    return response

def render_order_from_session(sess_order):
    order_temps = []
    for product_id, quantity in sess_order.items():
        product = product_service.find_product_by_id(product_id=product_id)
        order = {'id': product_id, 'product_id': product_id, 'product': product}
        order['quantity'] = int(quantity)
        order['price'] = product.price - round((product.price*product.sale)/100, 2)
        order_temps.append(order)
    return order_temps

