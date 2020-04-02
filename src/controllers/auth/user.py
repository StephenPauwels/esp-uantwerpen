from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, user_id, name, role, is_new):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.is_new = is_new

    def get_id(self):
        return self.user_id
