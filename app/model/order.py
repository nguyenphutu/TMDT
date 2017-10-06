from .base import Base
from app import db
from sqlalchemy.types import Enum

class OrderStatus(object):
    DatHang = '0'
    HuyDonHang = '1'
    DaGiaoHang = '2'
    DaNhanHang = '3'
    KhongGuiDuoc = '4'
    DoiTraHang = '5'

    enum = Enum(
        DatHang, HuyDonHang, DaGiaoHang, DaNhanHang, KhongGuiDuoc, DoiTraHang,
        name='order_status_enum'
    )


class Order(Base):
    __tablename__ = 'order'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='order', lazy=True)
    total_payment = db.Column(db.Float, nullable=False)
    status = db.Column(OrderStatus.enum, nullable=False, default=OrderStatus.DatHang)

    def __repr__(self):
        return '<order %r>' % (self.user)

class OrderDetail(Base):
    __tablename__ = 'order_details'

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order = db.relationship('Order', backref='order_details', lazy=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', lazy=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<order details %r>' % (self.order)