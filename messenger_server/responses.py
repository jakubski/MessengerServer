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
        def get_positive_response(cls, contacts_with_statuses):
            FLAG = 0

            return cls.PREFIX.to_bytes(PREFIX_SIZE, ENDIANNESS) + FLAG.to_bytes(FLAG_SIZE, ENDIANNESS) + DELIMITER + \
                   DELIMITER.join([DELIMITER.join((bytes(c[0], ENCODING), c[1].to_bytes(STATUS_SIZE, ENDIANNESS))) \
                                   for c in contacts_with_statuses])

        @classmethod
        def get_no_contacts_response(cls):
            FLAG = 1
            return cls.PREFIX.to_bytes(PREFIX_SIZE, ENDIANNESS) + FLAG.to_bytes(FLAG_SIZE, ENDIANNESS)

    class AddContactResponse:
        PREFIX = 0x04

        @classmethod
        def get_positive_response(cls, status):
            FLAG = 0
            return cls.PREFIX.to_bytes(PREFIX_SIZE, ENDIANNESS) + FLAG.to_bytes(FLAG_SIZE, ENDIANNESS) + DELIMITER + \
                   status.to_bytes(STATUS_SIZE, ENDIANNESS)

        @classmethod
        def get_user_not_found_response(cls):
            FLAG = 1
            return cls.PREFIX.to_bytes(PREFIX_SIZE, ENDIANNESS) + FLAG.to_bytes(FLAG_SIZE, ENDIANNESS)

    class StatusUpdateNotification:
        PREFIX = 0x05

        @classmethod
        def get_status_update_notification(cls, user, status):
            return cls.PREFIX.to_bytes(PREFIX_SIZE, ENDIANNESS) + bytes(user, ENCODING) + \
                   DELIMITER + status.to_bytes(STATUS_SIZE, ENDIANNESS)
