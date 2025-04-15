from datetime import datetime

class CartItemVM:
    def __init__(self, cart_id, order_id, user_id, product_id, quantity, unit_price, subtotal, created_at, updated_at):
        self.cart_id = cart_id
        self.order_id = order_id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.subtotal = subtotal
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "cart_id": str(self.cart_id),
            "order_id": str(self.order_id) if self.order_id else None,
            "user_id": str(self.user_id),
            "product_id": str(self.product_id),
            "quantity": self.quantity,
            "unit_price": str(self.unit_price),
            "subtotal": str(self.subtotal) if self.subtotal else None,
            "created_at": self.format_datetime(self.created_at),
            "updated_at": self.format_datetime(self.updated_at)
        }

    @staticmethod
    def from_dict(data):
        return CartItemVM(
            cart_id=data['cart_id'],
            order_id=data.get('order_id'),
            user_id=data['user_id'],
            product_id=data['product_id'],
            quantity=data['quantity'],
            unit_price=data['unit_price'],
            subtotal=data.get('subtotal'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    @staticmethod
    def format_datetime(value):
        """Helper function to format datetime or handle None/str values"""
        if isinstance(value, datetime):
            return value.isoformat()  # If it's a datetime object, use isoformat
        if isinstance(value, str):
            try:
                # If it's a string that can be parsed into a datetime, parse and return it
                parsed_datetime = datetime.fromisoformat(value)
                return parsed_datetime.isoformat()
            except ValueError:
                return value  # Return the string as is if it's not a valid datetime format
        return value  # If it's None or an unsupported type, return it as is
