class OrderItemVM:
    def __init__(self, product_id, quantity, unit_price):
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
        }

class OrderVM:
    def __init__(self, order_id, user_id, total_amount, order_status, shipping_address, order_items, created_at, updated_at):
        self.order_id = order_id
        self.user_id = user_id
        self.total_amount = total_amount
        self.order_status = order_status
        self.shipping_address = shipping_address
        self.order_items = [OrderItemVM(**item) for item in order_items]
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "total_amount": self.total_amount,
            "order_status": self.order_status,
            "shipping_address": self.shipping_address,
            "order_items": [item.to_dict() for item in self.order_items],
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @staticmethod
    def from_list(data_list):
        """Create list of OrderVM from a list of order dicts."""
        return [OrderVM(**item) for item in data_list]
