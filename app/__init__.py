from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_login import LoginManager
from flask_migrate import Migrate

# Define the WSGI application object
# app = Flask(__name__, static_url_path='/static')
csrf = CSRFProtect()
app = Flask(__name__)
csrf.init_app(app)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

# # Initial Migration
# migrate = Migrate(app, db)

###############
#### login ####
###############
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"


#######################
#### import module ####
#######################
from app.view.auth import auth as auth_module
from app.view.admin import admin as admin_module
from app.view.index import web as home_module
from app.view.products import product as product_module
from app.view.contact import contact as contact_module
from app.view.templates import template as template_module
from app.view.order import order as order_module

################
#### module ####
################
app.register_blueprint(auth_module)
app.register_blueprint(admin_module)
app.register_blueprint(home_module)
app.register_blueprint(product_module)
app.register_blueprint(contact_module)
app.register_blueprint(template_module)
app.register_blueprint(order_module)

db.create_all()

#jinjia2 config
from app.service.category import CategoryService
from app.service.orders import OrderTempService

@app.template_global(name='categories')
def categories():
    cate_survice = CategoryService(db)
    return cate_survice.all()
def get_time():
    import time
    return time.time()

def calculate_total_payment():
    order_temp_service = OrderTempService(db)
    orders = order_temp_service.all()
    total = 0
    for order in orders:
        total += order.price*order.quantity
    return round(total, 2)

app.jinja_env.globals['categories'] = categories
app.jinja_env.globals['get_time'] = get_time()
app.jinja_env.globals['calculate_total_payment'] = calculate_total_payment
