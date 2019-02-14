
DELIMITER = b'\r'
ENDIANNESS = "big"


class Responses:

    class SignUpResponse:
        PREFIX = 0x00

        @classmethod
        def get_positive_response(cls):
            FLAG = 0
            return cls.PREFIX.to_bytes(1, ENDIANNESS) + FLAG.to_bytes(1, ENDIANNESS)

        @classmethod
        def get_existing_login_response(cls):
            FLAG = 4
            return cls.PREFIX.to_bytes(1, ENDIANNESS) + FLAG.to_bytes(1, ENDIANNESS)

    class LogInResponse:
        PREFIX = 0x01

        @classmethod
        def get_positive_response(cls, key):
            FLAG = 0
            return cls.PREFIX.to_bytes(1, ENDIANNESS) + FLAG.to_bytes(1, ENDIANNESS) + DELIMITER + key.to_bytes(6, ENDIANNESS)

        @classmethod
        def get_wrong_login_response(cls):
            FLAG = 1
            return cls.PREFIX.to_bytes(1, ENDIANNESS) + FLAG.to_bytes(1, ENDIANNESS)

        @classmethod
        def get_wrong_password_response(cls):
            FLAG = 2
            return cls.PREFIX.to_bytes(1, ENDIANNESS) + FLAG.to_bytes(1, ENDIANNESS)

    class AddContactResponse:
        PREFIX = 0x04

        @classmethod
        def get_positive_response(cls):
            FLAG = 0
            return cls.PREFIX.to_bytes(1, ENDIANNESS) + FLAG.to_bytes(1, ENDIANNESS)

        @classmethod
        def get_user_not_found_response(cls):
            FLAG = 1
            return cls.PREFIX.to_bytes(1, ENDIANNESS) + FLAG.to_bytes(1, ENDIANNESS)
