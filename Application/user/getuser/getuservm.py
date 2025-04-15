class UserVM:
    def __init__(self, user_id, username, email, phone, address, city, state, zipcode, created_at):
        self.user_id = str(user_id)
        self.username = username
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.created_at = created_at

    def to_dict(self):
        """Convert UserVM instance to dictionary."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data):
        """Create UserVM instance from dictionary."""
        return UserVM(
            user_id=str(data.get("user_id")),
            username=data.get("username"),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            city=data.get("city"),
            state=data.get("state"),
            zipcode=data.get("zipcode"),
            created_at=data.get("created_at")
        )
