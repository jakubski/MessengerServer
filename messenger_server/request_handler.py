import socketserver
from database import DatabaseConnection, LoginTakenError, LoginNotFoundError, PasswordError
from user_management import UserManager
from responses import Responses


class InvalidRequestError(Exception):
    pass


class RequestHandler(socketserver.BaseRequestHandler):
    DELIMITER = '\r'

    def handle_signup_request(self, signup_request):
        try:
            email, login, password = signup_request.split(self.DELIMITER)
            DatabaseConnection().add_user(email, login, password)
            response = Responses.SignUpResponse.get_positive_response()
        except ValueError:
            raise InvalidRequestError()
        except LoginTakenError:
            response = Responses.SignUpResponse.get_existing_login_response()

        self.request.sendall(response)

    def handle_login_request(self, login_request):
        try:
            login, password = login_request.split(self.DELIMITER)
            DatabaseConnection().verify_login(login, password)
            key = UserManager.sign_in(login, self.request)
            response = Responses.LogInResponse.get_positive_response(key)
        except ValueError:
            raise InvalidRequestError()
        except LoginNotFoundError:
            response = Responses.LogInResponse.get_wrong_login_response()
        except PasswordError:
            response = Responses.LogInResponse.get_wrong_password_response()

        self.request.sendall(response)

    def handle_logout_request(self, logout_request):
        pass

    prefixes_to_methods = {
        0x00: handle_signup_request,
        0x01: handle_login_request,
        0x02: handle_logout_request,
    }

    def handle(self):
        while True:
            try:
                data = self.request.recv(1024)
                if data:
                    prefix = data[0]
                    handler_method = self.prefixes_to_methods[prefix]
                    handler_method(self, data[1:].decode("utf-8", "replace"))
            except (ConnectionResetError, ConnectionAbortedError):
                print("Zakończono połączenie.")
                break
