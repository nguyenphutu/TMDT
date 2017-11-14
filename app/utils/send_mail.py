from itsdangerous import URLSafeTimedSerializer
from app import app, mail, db
from flask import url_for, render_template
from flask_mail import Message, smtplib
from app.service.orders import OrderService

def send_invoice_email(order_id, user_email):
    order_service = OrderService(db)
    order = order_service.find_order_by_id(order_id)
    html = render_template(
        'view_order.html',
        order_date=order.date_created.strftime("%b %d %Y"),
        order_details=order.order_details
    )
    send_email('Your Invoice', [user_email], 'Invoice', html)

def send_email(subject, recipients, text_body, html_body):
    with mail.connect() as conn:
        msg = Message(subject, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        conn.send(msg)