class Responses:

    class SignUpResponse:
        @staticmethod
        def get_positive_response():
            prefix = 0x00
            flag = 0
            return prefix.to_bytes(1, "big") + flag.to_bytes(1, "big")

        @staticmethod
        def get_existing_login_response():
            prefix = 0x00
            flag = 4
            return prefix.to_bytes(1, "big") + flag.to_bytes(1, "big")

    class LogInResponse:
        @staticmethod
        def get_positive_response(key):
            prefix = 0x01
            flag = 0
            return prefix.to_bytes(1, "big") + flag.to_bytes(1, "big") + key.to_bytes(6, "big")

        @staticmethod
        def get_wrong_login_response():
            prefix = 0x01
            flag = 1
            return prefix.to_bytes(1, "big") + flag.to_bytes(1, "big")

        @staticmethod
        def get_wrong_password_response():
            prefix = 0x01
            flag = 2
            return prefix.to_bytes(1, "big") + flag.to_bytes(1, "big")
