class GetOrderHistoryVM:
    def __init__(self, order_id, user_id, shipping_address, order_status):
        self.order_id = order_id
        self.user_id = user_id
        self.shipping_address = shipping_address
        self.order_status = order_status

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "shipping_address" : self.shipping_address,
            "order_status": self.order_status
        }

    @staticmethod
    def from_dict(data):
        return GetOrderHistoryVM(
            order_id=data.get("order_id"),
            user_id=data.get("user_id"),
            shipping_address=data.get("shipping_address"),
            order_status=data.get("order_status")
        )
