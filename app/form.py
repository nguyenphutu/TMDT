
# Import Form elements such as TextField and BooleanField (optional)
from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo


# Define the login form (WTForms)

class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.Length(min=6, max=50)])

class RegistrationForm(Form):

    first_name = StringField('First Name', [validators.Length(min=4, max=25)])
    last_name = StringField('Last Name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [[validators.Length(min=6, max=35)]])

class CreateAccount(Form):

    first_name = StringField('First Name', [validators.Length(min=4, max=25)])
    last_name = StringField('Last Name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    role = StringField('Role', [validators.Length(min=1, max=10)])
    password = PasswordField('New Password', [[validators.Length(min=6, max=35)]])

class CheckoutForm(Form):
    fullname = StringField('Full Name', [validators.Length(min=4, max=255)])
    city = StringField('City', [validators.Length(min=2, max=255)])
    district = StringField('District', [validators.Length(min=2, max=255)])
    ward = StringField('Ward', [validators.Length(min=2, max=255)])
    address = StringField('Address', [validators.Length(min=2, max=255)])
    phone = StringField('Phone', [validators.Length(min=9, max=12)])
class ForgotForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
