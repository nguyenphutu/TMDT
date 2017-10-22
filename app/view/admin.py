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
@admin_required
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
            flash(u'Delete account successfully', 'success')
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
                    flash(u'Update account successfully', 'success')
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
                return render_template("admin_products.html", products=products, add_status=add_status)
            image = request.files['file_image']
            if image and allowed_file(image.filename):
                product_img_name = product.slug + '.jpg'
                image.save(os.path.join('app/static/products/', product_img_name))
                # image.save(os.path.join(url_for('static', filename='products/'), product_img_name))
                add_status = 'success'
                return render_template("admin_products.html", products=products, add_status=add_status)
            add_status = 'warring'
            return render_template("admin_products.html", products=products, add_status=add_status)
        else:
            add_status = 'error'
            return render_template("admin_products.html", products=products, add_status=add_status)
    return render_template("admin_products.html", products=products)

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
            if product:
                product_img_name = product.slug + '.jpg'
                os.remove(os.path.join('app/static/products/', product_img_name))
                flash(u'Delete product successfully', 'success')
                return redirect(url_for('admin.list_products'))
            abort(404)
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
                            product_img_name = product.slug + '.jpg'
                            image.save(os.path.join('app/static/products/', product_img_name))
                            # image.save(os.path.join(url_for('static', filename='products/'), product_img_name))
                            flash(u'Update product successfully', 'success')
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

@admin.route('/products/<category>', methods=['GET', 'POST'])
@login_required
@manage_required
def list_cate_products(category):
    product_service = ProductService(db=db)
    cate_service = CategoryService(db=db)
    products = cate_service.get_product_of_cate(category_name=category.lower())
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category']
        price = request.form['price']
        quantity = request.form['quantity']
        info = request.form['info']
        product = product_service.create_product(name=name, category_id=category_id, price=price, quantity=quantity, info=info)
        if product:
            products = cate_service.get_product_of_cate(category_name=category.lower())
            if ('file_image' not in request.files) or (request.files["file_image"].filename == ''):
                add_status = 'warring'
                return render_template("admin_products.html", products=products, category=category.lower(), add_status=add_status)
            image = request.files['file_image']
            if image and allowed_file(image.filename):
                product_img_name = product.slug + '.jpg'
                image.save(os.path.join('app/static/products/', product_img_name))
                # image.save(os.path.join(url_for('static', filename='products/'), product_img_name))
                add_status = 'success'
                return render_template("admin_products.html", products=products, category=category.lower(), add_status=add_status)
            add_status = 'warring'
            return render_template("admin_products.html", products=products, category=category.lower(), add_status=add_status)
        else:
            add_status = 'error'
            return render_template("admin_products.html", products=products, category=category.lower(), add_status=add_status)
    return render_template("admin_products.html", products=products, category=category.lower())

@admin.route('/products/<category>/<id>/<action>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@manage_required

def action_cate_products(category, id, action):
    product_service = ProductService(db)
    if id and action.lower() == 'delete':
        if request.method == 'POST':
            product = product_service.delete(id=id)
            if product:
                product_img_name = product.slug + '.jpg'
                os.remove(os.path.join('app/static/products/', product_img_name))
                flash(u'Delete product successfully', 'success')
                return redirect(url_for('admin.list_cate_products', category=category))
            abort(404)
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
                pro = product_service.change_product(product_id=product.id, name=name, category_id=category_id,
                                                     price=price,
                                                     quantity=quantity, info=info, sale=sale)
                if pro:
                    if 'file_image' in request.files and request.files['file_image'].filename != '':
                        image = request.files['file_image']
                        if image and allowed_file(image.filename):
                            product_img_name = product.slug + '.jpg'
                            image.save(os.path.join('app/static/products/', product_img_name))
                            # image.save(os.path.join(url_for('static', filename='products/'), product_img_name))
                            flash(u'Update product successfully', 'success')
                            return redirect(url_for('admin.list_cate_products', category=category))

                    flash(u'Update product success', 'success')
                    return redirect(url_for('admin.list_cate_products', category=category))
                else:
                    return render_template("edit_product.html", product=product, error='Error product name or some field please update again')
            else:
                return render_template("edit_product.html", product=product)
        else:
            abort(404)

    abort(404)

@admin.route('/category', methods=['GET', 'POST'])
@login_required
@manage_required
def list_category():
    cate_survice = CategoryService(db)
    if request.method == 'POST':
        name = request.form['name']
        cate = cate_survice.create_category(name=name)
        if cate:
            add_status = 'success'
            return render_template("admin_category.html", add_status=add_status)
        else:
            add_status = 'error'
            return render_template("admin_category.html", add_status=add_status)
    return render_template("admin_category.html")

@admin.route('/category/<id>/<action>', methods=['GET', 'POST'])
@login_required
@manage_required
def action_cates(id, action):
    cate_survice = CategoryService(db)
    if id and action.lower() == 'delete':
        if request.method == 'POST':
            cate = cate_survice.delete_cate(id=id)
            if cate:
                flash(u'Delete category successfully', 'success')
                return redirect(url_for('admin.list_category'))
            abort(404)
        else:
            abort(404)
    if id and action.lower() == 'edit':
        cate = cate_survice.find_cate_by_id(id=id)
        if cate:
            if request.method == 'POST':
                name = request.form['name']
                url = request.form['url']
                new_cate = cate_survice.change_category(id=cate.id, name=name, url=url)
                if new_cate:
                    flash(u'Update account successfully', 'success')
                    return redirect(url_for('admin.list_category'))
                else:
                    return render_template("edit_cate.html", cate=cate, error='Error email or some field please update again')
            else:
                return render_template("edit_cate.html", cate = cate)
        else:
            abort(404)

    abort(404)