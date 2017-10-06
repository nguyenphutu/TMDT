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