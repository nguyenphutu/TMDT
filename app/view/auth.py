from flask import render_template, Blueprint, request, redirect, url_for, g
from app import db, login_manager
from app.service.user import UserService, UserDetailService
from app.form import LoginForm, RegistrationForm
from flask_login import login_required, login_user, current_user, logout_user, UserMixin
from app.model.user import User

auth = Blueprint('auth', __name__, url_prefix='/auth')

# # Sample user
# class _User(UserMixin):
#     pass
#

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@auth.before_request
def before_request():
    g.user = current_user



@auth.route('/register', methods = ['POST', 'GET'])
def register():
    error = None
    form = RegistrationForm()
    if request.method == 'POST':
        u_service = UserService(db)
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        user = u_service.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
        print(user)
        if user:
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user=user, remember=True)
            return redirect(url_for('web.homepage'))
        else:
            error = "Email is already exists"
    else:
        return render_template("register.html", form=form, error=error)

@auth.route('/login', methods = ['POST', 'GET'])
def login():
    error = None
    print(g.user)
    form = LoginForm()
    if request.method == 'POST':
        u_service = UserService(db)
        email = request.form['email']
        password = request.form['password']
        if u_service.validate(email=email, password=password):
            user = u_service.find_by_email(email)
            user.authenticated = True
            db.session.commit()
            login_user(user=user, remember=True)
            return redirect(url_for('web.homepage'))
        else:
            error = 'Invalid username/password'
    return render_template("login.html", form=form, error = error)

@auth.route("/logout", methods=["get"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/profile", methods=["GET"])
@login_required
def profile():
    return render_template("login.html")