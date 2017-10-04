from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


# Define the WSGI application object
# app = Flask(__name__, static_url_path='/static')
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# # Initial Migration
# migrate = Migrate(app, db)

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
