import socketserver
from database import DatabaseConnection, LoginTakenError
from responses import Responses


class InvalidRequestError(Exception):
    pass


class RequestHandler(socketserver.BaseRequestHandler):
    DELIMITER = '\r'

    def handle_signup_request(self, request):
        try:
            email, login, password = request.split(self.DELIMITER)
            db = DatabaseConnection()
            db.add_user(email, login, password)
            response = Responses.SignUpResponse.get_positive_response()
        except ValueError:
            raise InvalidRequestError()
        except LoginTakenError:
            response = Responses.SignUpResponse.get_existing_login_response()

        self.request.sendall(response)

    def handle_login_request(self, request):
        pass

    def handle_logout_request(self, request):
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
