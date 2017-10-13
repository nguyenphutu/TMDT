from flask import render_template, Blueprint, request, redirect, url_for, g
from app import db, login_manager
from app.service.user import UserService
from app.form import LoginForm, RegistrationForm, ForgotForm
from flask_login import login_required, login_user, current_user, logout_user
from app.model.user import User

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/accounts', methods=['GET'])
def list_accounts():
    u_service = UserService(db)
    accouts = u_service.all()

    return render_template("list_accouts.html", accouts=accouts)

@admin.route('/create_manager', methods = ['POST', 'GET'])
def create_manager():
    form = RegistrationForm()
    if request.method == 'POST':
        u_service = UserService(db)
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        user = u_service.create_user(first_name=first_name, last_name=last_name, email=email, password=password, role=role)
        if user:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('admin.list_manager'))
        else:
            error = "Email is already exists"
            return render_template("create_manager.html", form=form, error=error)
    else:
        return render_template("create_manager.html", form=form)
