from flask import Flask, render_template, Blueprint
from flask_login import current_user

web = Blueprint('web', __name__, url_prefix='/')

@web.route('/')
def homepage():
    print(current_user.is_authenticated)
    return render_template("index.html")

