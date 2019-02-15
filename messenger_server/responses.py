from messenger_server.config import *


class Responses:

    class SignUpResponse:
        PREFIX = 0x00

        @classmethod
        def get_positive_response(cls):
            FLAG = 0
            return cls.PREFIX.to_bytes(PREFIX_SIZE, ENDIANNESS) + FLAG.to_bytes(FLAG_SIZE, ENDIANNESS)

        @classmethod
        def get_existing_login_response(cls):
            FLAG = 4
            return cls.PREFIX.to_bytes(PREFIX_SIZE, ENDIANNESS) + FLAG.to_bytes(FLAG_SIZE, ENDIANNESS)

    class LogInResponse:
        PREFIX = 0x01

        @classmethod
        def get_positive_response(cls, key):
            FLAG = 0
            return cls.PREFIX.to_bytes(PREFIX_SIZE, ENDIANNESS) + FLAG.to_bytes(FLAG_SIZE, ENDIANNESS) + \
                   DELIMITER + key.to_bytes(KEY_SIZE, ENDIANNESS)

        @classmethod
        def get_wrong_login_response(cls):
            FLAG = 1
            return cls.PREFIX.to_bytes(PREFIX_SIZE, ENDIANNESS) + FLAG.to_bytes(FLAG_SIZE, ENDIANNESS)

        @classmethod
        def get_wrong_password_response(cls):
            FLAG = 2
            return cls.PREFIX.to_bytes(PREFIX_SIZE, ENDIANNESS) + FLAG.to_bytes(FLAG_SIZE, ENDIANNESS)

    class GetContacts:
        PREFIX = 0x03

        @classmethod
        def get_positive_response(cls, contacts):
            FLAG = 0

            return cls.PREFIX.to_bytes(PREFIX_SIZE, ENDIANNESS) + FLAG.to_bytes(FLAG_SIZE, ENDIANNESS) + \
                   DELIMITER + bytes(DELIMITER_STR.join(contacts), "utf-8")

        @classmethod
        def get_no_contacts_response(cls):
            FLAG = 1
            return cls.PREFIX.to_bytes(PREFIX_SIZE, ENDIANNESS) + FLAG.to_bytes(FLAG_SIZE, ENDIANNESS)

    class AddContactResponse:
        PREFIX = 0x04

        @classmethod
        def get_positive_response(cls):
            FLAG = 0
            return cls.PREFIX.to_bytes(PREFIX_SIZE, ENDIANNESS) + FLAG.to_bytes(FLAG_SIZE, ENDIANNESS)

        @classmethod
        def get_user_not_found_response(cls):
            FLAG = 1
            return cls.PREFIX.to_bytes(PREFIX_SIZE, ENDIANNESS) + FLAG.to_bytes(FLAG_SIZE, ENDIANNESS)
