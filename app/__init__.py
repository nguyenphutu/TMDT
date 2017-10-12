from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_login import LoginManager

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

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

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
from app.view.index import web as home_module
from app.view.products import product as product_module
from app.view.contact import contact as contact_module

################
#### module ####
################
app.register_blueprint(auth_module)
app.register_blueprint(home_module)
app.register_blueprint(product_module)
app.register_blueprint(contact_module)

db.create_all()
