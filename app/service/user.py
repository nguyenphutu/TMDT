from app.model.user import User

class UserService():
    def __init__(self, db):
        self.db = db

    def create_user(self, first_name, last_name, password, email, role, status):
        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.password = password
        user.email = email
        user.role = role
        user.status = status

        try:
            self.db.session.add(user)
            self.db.session.commit()
        except Exception as e:
            status = 'Email is already exists'
            self.db.session.rollback()
        if status:
            return status
        return user

    def update_user(self, user_id, first_name, last_name, email, role, status):
        user = User.query.filter_by(id=user_id).first()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.role = role
        user.status = status
        self.db.session.commit()

    def delete_user(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            self.db.session.delete(user)
            self.db.session.commit()
            return 'success'
        return 'Error'

    def all(self):
        return User.query.all()\

    def find_by_email(self, email):
        user = User.query.filter_by(email=email).first()
        if user:
            return user
        return None