from random import randrange


class OnlineUser:
    def __init__(self, login, key, socket):
        self.login = login
        self.key = key
        self.socket = socket


class UserManager:
    _range = 1048575
    _online_users = []

    @classmethod
    def get_online_user_by_key(cls, key):
        for user in cls._online_users:
            if user.key == key:
                return user

        return None

    @classmethod
    def sign_in(cls, login, socket):
        key = int()

        while True:
            key = randrange(0, cls._range)
            if cls.get_online_user_by_key(key) is None:
                break

        cls._online_users.append(OnlineUser(login, key, socket))

        return key
