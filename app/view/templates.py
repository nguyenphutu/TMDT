from flask import Blueprint
from app import app, db
from app.service.category import CategoryService


template = Blueprint('template', __name__, url_prefix='/jinja2_template')

def categories():
    cate_survice = CategoryService(db)
    return cate_survice.all()
def main():
    app.jinja_env.globals['categories'] = categories()