from app.model.category import Category

class CategoryService():
    def __init__(self, db):
        self.db = db

    def all(self):
        return Category.query.all()

    def create_category(self, name):
        category = Category()
        category.name = name
        category.url = '_'.join(name.split()).lower()
        try:
            self.db.session.add(category)
            self.db.session.commit()
            return category
        except Exception as e:
            status = 'Category is already exists'
            self.db.session.rollback()
            return None

    def change_category(self, id , name, url=None):
        category = Category.query.filter_by(id=id).first()
        if category:
            category.name = name
            category.url = url
            self.db.session.commit()
            return category
        return None

    def find_cate_by_name(self, category_name):
        category = Category.query.filter_by(name=category_name).first()
        if category:
            return category
        return None

    def find_cate_by_id(self, id):
        category = Category.query.filter_by(id=id).first()
        if category:
            return category
        return None

    def get_product_of_cate(self, category_name):
        category = Category.query.filter_by(name=category_name).first()
        if category:
            return category.products
        return []

    def delete_cate(self, id):
        cate = Category.query.filter_by(id=id).first()
        if cate:
            self.db.session.delete(cate)
            self.db.session.commit()
            return cate
        return None