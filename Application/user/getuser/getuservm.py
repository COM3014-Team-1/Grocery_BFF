class UserVM:
    def __init__(self, user_id, name, email, phone, address, city, state, zipcode, created_at):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data['user_id'],
            data['name'],
            data['email'],
            data.get('phone'),
            data.get('address'),
            data.get('city'),
            data.get('state'),
            data.get('zipcode'),
            data['created_at']
        )
