from app.model.order import Order, OrderDetail
from .user import UserService
from .products import ProductService

class OrderService():

    def __init__(self, db):
        self.db = db

    def create_order(self, user_id, status):
        order = Order()
        user_service = UserService(self.db)
        order.user = user_service.find_user_by_id(user_id)
        order.status = status

        try:
            self.db.add(order)
            self.db.commit()
            return order
        except Exception as e:
            return "Error, create order error try again"

    def update_order(self, order_id, status):
        order = Order.query.filter_by(id=order_id).first()
        if order:
            order.status = status
            self.db.commit()
        else:
            return "Error, update order error try again"

    def delete_order(self, order_id):
        order = Order.query.filter_by(id=order_id).first()
        if order:
            self.db.delete(order)
            self.db.commit()
        else:
            return "Error, no order to delete"

class OrderDetailService():

    def __init__(self, db):
        self.db = db

    def create_order_detail(self, order_id, product_id, quantity, price):
        order_detail = OrderDetail()

        order = Order.query.filter_by(id=order_id).first()
        order_detail.order_id = order_id
        order_detail.order = order
        order_detail.quantity = quantity

        order_detail.product_id = product_id
        product_service = ProductService(self.db)
        product = product_service.find_product_by_id(product_id)
        order_detail.product = product
        order_detail.price = price

        try:
            self.db.add(order_detail)
            self.db.commit()
        except Exception as e:
            return "Error, can't create order"

    def delete_order_detail(self, order_detail_id):
        order_detail = OrderDetail.query.filter_by(id=order_detail_id).first()
        if order_detail:
            self.db.delete(order_detail)
            self.db.commit()
        else:
            return "Error, no order detail"



