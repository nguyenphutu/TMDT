from flask import render_template, Blueprint, request, redirect, url_for, abort, flash
from app import db, login_manager
from app.service.user import UserService
from app.form import LoginForm, RegistrationForm, ForgotForm, CreateAccount
from flask_login import login_required, login_user, current_user, logout_user
from app.model.user import User
from app.service.category import CategoryService
from app.service.products import ProductService
from .scripts import admin_required, manage_required
import os
import time

admin = Blueprint('admin', __name__, url_prefix='/admin')

ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin.route('/', methods=['GET'])
@login_required
@manage_required
def dashboard():
    u_service = UserService(db)
    p_service = ProductService(db)
    n_accounts = len(u_service.all())
    n_products = len(p_service.all())

    return render_template("dashboard.html", n_accounts=n_accounts, n_products=n_products)


@admin.route('/account', methods=['GET','POST'])
@login_required
# @admin_required
@manage_required
def list_accounts():
    u_service = UserService(db)
    accounts = u_service.all()
    add_status = ''
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']
        user = u_service.create_user(first_name=first_name, last_name=last_name, email=email, password=password, role=role)
        if user:
            add_status = 'success'
            accounts = u_service.all()
            return render_template("admin_accounts.html", accounts=accounts, add_status=add_status)
        else:
            add_status = 'error'
            return render_template("admin_accounts.html", accounts=accounts, add_status=add_status)
    return render_template("admin_accounts.html", accounts=accounts, add_status=add_status)


@admin.route('/account/<id>/<action>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@admin_required
def action_accounts(id, action):
    u_service = UserService(db)
    if id and action.lower() == 'delete':
        if request.method == 'POST':
            user = u_service.delete_user(user_id=id)
            return redirect(url_for('admin.list_accounts'))
        else:
            abort(404)
    if id and action.lower() == 'edit':
        user = u_service.find_user_by_id(user_id=id)
        if user:
            if request.method == 'POST':
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                email = request.form['email']
                role = request.form['role']
                account = u_service.update_user(user_id=user.id, first_name=first_name, last_name=last_name, email=email, role=role)
                if account:
                    flash(u'Update account success', 'success')
                    return redirect(url_for('admin.list_accounts'))
                else:
                    return render_template("create_manager.html", account=user, error='Error email or some field please update again')
            else:
                return render_template("create_manager.html", account = user)
        else:
            abort(404)

    abort(404)

@admin.route('/products', methods=['GET', 'POST'])
@login_required
@manage_required

def list_products():
    product_service = ProductService(db=db)
    category_service = CategoryService(db=db)
    categorys = category_service.all()
    products = product_service.all()
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category']
        price = request.form['price']
        quantity = request.form['quantity']
        info = request.form['info']
        product = product_service.create_product(name=name, category_id=category_id, price=price, quantity=quantity, info=info)
        if product:
            products = product_service.all()
            if ('file_image' not in request.files) or (request.files["file_image"].filename == ''):
                add_status = 'warring'
                return render_template("admin_products.html", products=products, add_status=add_status, categorys=categorys)
            image = request.files['file_image']
            if image and allowed_file(image.filename):
                filename = product.slug + '.jpg'
                image.save(os.path.join('app/static/products', filename))
                add_status = 'success'
                return render_template("admin_products.html", products=products, add_status=add_status, categorys=categorys)
            add_status = 'warring'
            return render_template("admin_products.html", products=products, add_status=add_status, categorys=categorys)
        else:
            add_status = 'error'
            return render_template("admin_products.html", products=products, add_status=add_status, categorys=categorys)
    return render_template("admin_products.html", products=products, categorys=categorys, time=time.time())

@admin.route('/products/<id>/<action>', methods=['GET', 'POST'])
@login_required
@manage_required
def action_product(id, action):
    product_service = ProductService(db)
    category_service = CategoryService(db=db)
    categorys = category_service.all()
    if id and action.lower() == 'delete':
        if request.method == 'POST':
            product = product_service.delete(id=id)
            return redirect(url_for('admin.list_products'))
        else:
            abort(404)
    if id and action.lower() == 'edit':
        product = product_service.find_product_by_id(product_id=id)
        if product:
            if request.method == 'POST':
                name = request.form['name']
                category_id = request.form['category']
                price = request.form['price']
                quantity = request.form['quantity']
                info = request.form['info']
                sale = request.form['sale']
                if sale == '':
                    sale = 0
                pro = product_service.change_product(product_id=product.id, name=name, category_id=category_id, price=price,
                                                     quantity=quantity, info=info, sale=sale)
                print(pro)
                if pro:
                    if 'file_image' in request.files and request.files['file_image'].filename != '':
                        image = request.files['file_image']
                        if image and allowed_file(image.filename):
                            filename = product.slug + '.jpg'
                            image.save(os.path.join('app/static/products', filename))
                            flash(u'Update product success', 'success')
                            return redirect(url_for('admin.list_products'))

                    flash(u'Update product success', 'success')
                    return redirect(url_for('admin.list_products'))
                else:
                    return render_template("edit_product.html", categorys=categorys, product=product, error='Error product name or some field please update again')
            else:
                return render_template("edit_product.html", categorys=categorys, product=product)
        else:
            abort(404)

    abort(404)

@admin.route('/products/<category>', methods=['GET'])
@login_required
@manage_required

def list_cate_products(category):
    cate_service = CategoryService(db=db)
    products = cate_service.get_product_of_cate(category_name=category.lower())
    return render_template("admin_products.html", products=products, category=category.title())

@admin.route('/products/<category_name>/<id>/<action>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@manage_required

def action_cate_products(category_name, id, action):
    cate_service = CategoryService(db=db)
    category = cate_service.find_cate_by_name(category_name=category_name)
    if action.lower() == 'edit':
        pass
    if action.lower() == 'delete':
        pass
    return url_for("admin.list_cate_products", category=category_name.title())
