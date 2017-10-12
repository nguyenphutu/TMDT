from app.model.user import User, User_Detail

class UserService():
    def __init__(self, db):
        self.db = db

    def create_user(self, first_name, last_name, password, email, role=None, status=None):
        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.role = role
        user.status = status
        user.set_password(password)

        message = ''
        try:
            self.db.session.add(user)
            self.db.session.commit()
        except Exception as e:
            message = 'Email is already exists'
            self.db.session.rollback()
        if message != '':
            return {'masage': message}
        return {'user': user}

    def update_user(self, user_id, first_name, last_name, email, role=None, status=None):
        user = User.query.filter_by(id=user_id).first()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.role = role
        user.status = status
        self.db.session.commit()

    def change_password(self, user_id, old_password, new_password):
        user = User.query.filter_by(id=user_id).first()
        if user.check_password(password=old_password) :
            user.set_password(password=new_password)
            self.db.session.commit()
        else:
            return 'Error PassWord'
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

    def find_user_by_id(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            return user
        else:
            return None

    def validate(self, email, password):
        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password=password):
                return 1
        return 0


class UserDetailService():
    def __init__(self, db):
        self.db = db

    def create_user_detail(self, city, district, ward, address, phone, date_of_birth, gender, user_id, user ):
        user_detail = User_Detail()
        user_detail.city = city
        user_detail.district = district
        user_detail.ward = ward
        user_detail.address = address
        user_detail.phone = phone
        user_detail.date_of_birth = date_of_birth
        user_detail.gender = gender
        user_detail.user_id = user_id
        user_detail.user = user

        try:
            self.db.add(user_detail)
            self.db.commit()
            return user_detail
        except Exception as e:
            return 'Error, add user detail have some error'


    def update_user_detail(self, user_id, city, district, ward, address, phone, date_of_birth, gender):
        user_detail = User.query.filter_by(id=user_id).first().user_detail
        if user_detail:
            user_detail.city = city
            user_detail.district = district
            user_detail.ward = ward
            user_detail.address = address
            user_detail.phone = phone
            user_detail.date_of_birth = date_of_birth
            user_detail.gender = gender

            self.db.commit()
        else:
            return 'Error, no user or update have some error'
