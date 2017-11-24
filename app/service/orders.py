from app.model.order import Order, OrderDetail, OrderTemp
from .user import UserService
from .products import ProductService

class OrderService():

    def __init__(self, db):
        self.db = db
        self.user_service = UserService(db)

    def all(self):
        return Order.query.all()

    def get_new_order(self):
        return Order.query.filter_by(status='0').order_by(Order.date_created).all()

    def create_order(self, user_id):
        order = Order()
        order.user = self.user_service.find_user_by_id(user_id)
        try:
            self.db.session.add(order)
            self.db.session.commit()
            return order
        except Exception as e:
            # return "Error, create order error try again"
            return None
    def update_order(self, order_id, status):
        order = Order.query.filter_by(id=order_id).first()
        if order:
            order.status = status
            self.db.session.commit()
            return order
        else:
            # return "Error, update order error try again"
            return None
    def delete_order(self, order_id):
        order = Order.query.filter_by(id=order_id).first()
        if order:
            self.db.session.delete(order)
            self.db.session.commit()
            return 1
        else:
            # return "Error, no order to delete"
            return 0
    def find_order_by_id(self, order_id):
        order = Order.query.filter_by(id=order_id).first()
        if order:
            return order
        else:
            return None
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
        order_detail.price = price
        product_service = ProductService(self.db)
        product = product_service.find_product_by_id(product_id=product_id)
        order_detail.product = product

        try:
            self.db.session.add(order_detail)
            self.db.session.commit()
            return order_detail
        except Exception as e:
            # return "Error, can't create order"
            return None

    def delete_order_detail(self, order_detail_id):
        order_detail = OrderDetail.query.filter_by(id=order_detail_id).first()
        if order_detail:
            self.db.session.delete(order_detail)
            self.db.session.commit()
            return 1
        else:
            return 0

class OrderTempService():
    def __init__(self, db):
        self.db = db
        self.user_service = UserService(db)
        self.product_service = ProductService(db)

    def all(self, user_id):
        orders = OrderTemp.query.filter_by(user_id=user_id).order_by(OrderTemp.id).all()
        return orders
    def create_order_temp(self, user_id, product_id, quantity, price):
        order_temp = OrderTemp()
        user = self.user_service.find_user_by_id(user_id)
        order_temp.user_id = user_id
        order_temp.user = user
        order_temp.quantity = quantity
        order_temp.price = price
        order_temp.product_id = product_id
        product = self.product_service.find_product_by_id(product_id)
        order_temp.product = product

        try:
            self.db.session.add(order_temp)
            self.db.session.commit()
            return order_temp
        except Exception as e:
            return None

    def delete_order_temp_by_id(self, order_temp_id):
        order_temp = OrderTemp.query.filter_by(id=order_temp_id).first()
        if order_temp:
            self.db.session.delete(order_temp)
            self.db.session.commit()
            return 1
        else:
            return 0

    def delete_order_temps(self):
        order_temps = OrderTemp.query.all()
        if order_temps:
            for order in order_temps:
                self.db.session.delete(order)
                self.db.session.commit()
            return 1
        return 0

    def find_order_by_product_id(self,user_id,  product_id):
        order_temp = OrderTemp.query.filter_by(product_id=product_id,
                                               user_id=user_id).first()
        if order_temp:
            return order_temp.id
        return None

    def update(self, order_temp_id, quantity):
        order_temp = OrderTemp.query.filter_by(id=order_temp_id).first()

        if order_temp and int(quantity) <= order_temp.product.quantity:
            order_temp.quantity = quantity
            self.db.session.commit()
            return order_temp
        return None