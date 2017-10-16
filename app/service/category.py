from app.model.category import Category

class CategoryService():
    def __init__(self, db):
        self.db = db

    def create_category(self, name):
        category = Category()
        category.name = name
        category.url = '_'.join(name.split()).lower()
        status = ''
        try:
            self.db.session.add(category)
            self.db.session.commit()
        except Exception as e:
            status = 'Category is already exists'
            self.db.session.rollback()
        if status != '':
            return status
        return category

    def find_cate_by_name(self, category_name):
        category = Category.query.filter_by(name=category_name)
        if category:
            return category
        return None

    def get_product_of_cate(self, category_name):
        category = Category.query.filter_by(name=category_name).first()
        if category:
            return category.products
        return []