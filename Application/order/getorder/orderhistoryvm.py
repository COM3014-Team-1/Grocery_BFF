class GetOrderHistoryVM:
    def __init__(self, order_id, user_id, shipping_address, order_status, order_items, total_amount):
        self.order_id = order_id
        self.user_id = user_id
        self.shipping_address = shipping_address
        self.order_status = order_status
        self.order_items = order_items 
        self.total_amount = total_amount

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "shipping_address": self.shipping_address,
            "order_status": self.order_status,
            "order_items": self.order_items,
            "total_amount": self.total_amount
        }

    @staticmethod
    def from_dict(data):
        return GetOrderHistoryVM(
            order_id=data.get("order_id"),
            user_id=data.get("user_id"),
            shipping_address=data.get("shipping_address"),
            order_status=data.get("order_status"),
            order_items=data.get("order_items", []),  # Safely default to an empty list
            total_amount=data.get("total_amount")
        )
