from flask import Flask, render_template, Blueprint

contact = Blueprint('contact', __name__, url_prefix='/contact')

@contact.route('/')
def contact_us():
    return render_template("contact.html")
