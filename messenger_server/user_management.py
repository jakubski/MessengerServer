from random import randrange
from messenger_server.config import DELIMITER, KEY_SIZE, ENDIANNESS


class OnlineUser:
    def __init__(self, login, key, socket):
        self.login = login
        self.key = key
        self.socket = socket


class UserManager:
    _range = 4_294_967_294
    _online_users = []

    @classmethod
    def get_online_user_by_key(cls, key):
        for user in cls._online_users:
            if user.key == key:
                return user

        return None

    @classmethod
    def get_online_user_by_login(cls, login):
        for user in cls._online_users:
            if user.login == login:
                return user

        return None

    @classmethod
    def sign_in(cls, login, socket):
        key = int()

        while True:
            key = randrange(0, cls._range)
            if (cls.get_online_user_by_key(key) is None) and \
               (key.to_bytes(KEY_SIZE, ENDIANNESS).find(DELIMITER) < 0):
                break

        user = OnlineUser(login, key, socket)
        cls._online_users.append(user)

        return user
