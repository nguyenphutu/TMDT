from app import app, db
from app.service.category import CategoryService

@app.template_global(name='categories')
def categories():
    cate_survice = CategoryService(db)
    return cate_survice.all()

def main_config_jinja2():
    app.jinja_env.globals['categories'] = categories