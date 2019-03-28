"""The following classes are oriented toward working with users as they are signed-in
(i.e. have established a socket connection with the server and authenticated themselves)."""
from random import randrange
from messenger_server.config import DELIMITER, KEY_SIZE, ENDIANNESS


class OnlineUser:
    """Class represents a user at the time of being signed-in.

    :param login: User's login
    :type login: str
    :param key: User's identification key
    :type key: int
    :param socket: Socket established between the user and the server
    :type socket: :py:class:`socket.socket`
    """
    def __init__(self, login, key, socket):
        self.login = login
        self.key = key
        self.socket = socket


class UserManager:
    """This class keeps track of users currently logged in."""
    _range = 4_294_967_294
    _online_users = []

    @classmethod
    def get_online_user_by_key(cls, key):
        """Get online user with matching identification key.

        :param key: Identification key
        :type key: int
        :return: Online user whose key has been matched
        :rtype: :py:class:`messenger_server.user_management.OnlineUser` or None
        """
        for user in cls._online_users:
            if user.key == key:
                return user

        return None

    @classmethod
    def get_online_user_by_login(cls, login):
        """Get online user with matching login.

        :param login: User's login
        :type login: str
        :return: Online user whose login has been matched
        :rtype: :py:class:`messenger_server.user_management.OnlineUser` or None
        """
        for user in cls._online_users:
            if user.login == login:
                return user

        return None

    @classmethod
    def sign_in(cls, login, socket):
        """Generate unique identification key and add new online user.

        :param login: User's login
        :type login: str
        :param socket: Socket established between the user and the server
        :type socket: :py:class:`socket.socket`
        :return: Online user with newly generated key
        :rtype: :py:class:`messenger_server.user_management.OnlineUser`
        """
        key = int()

        while True:
            key = randrange(0, cls._range)
            if (cls.get_online_user_by_key(key) is None) and \
               (key.to_bytes(KEY_SIZE, ENDIANNESS).find(DELIMITER) < 0):
                break

        user = OnlineUser(login, key, socket)
        cls._online_users.append(user)

        return user
