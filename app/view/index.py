from flask import Flask, render_template, Blueprint
web = Blueprint('web', __name__, url_prefix='/')

@web.route('/')
def homepage():
    return render_template("index.html")

