import socketserver
from messenger_server.database import *
from messenger_server.user_management import UserManager
from messenger_server.responses import Responses
from messenger_server.config import *


class InvalidRequestError(Exception):
    pass


class RequestHandler(socketserver.BaseRequestHandler):

    def handle_signup_request(self, signup_request):
        try:
            email, login, password = signup_request.decode("utf-8", "replace").split(DELIMITER)
            DatabaseConnection().add_user(email, login, password)
            response = Responses.SignUpResponse.get_positive_response()
        except ValueError:
            raise InvalidRequestError()
        except LoginTakenError:
            response = Responses.SignUpResponse.get_existing_login_response()

        self.request.sendall(response)

    def handle_login_request(self, login_request):
        try:
            login, password = login_request.decode("utf-8", "replace").split(DELIMITER)
            DatabaseConnection().verify_login(login, password)
            key = UserManager.sign_in(login, self.request)
            response = Responses.LogInResponse.get_positive_response(key)
            # notify users who have this user in their contacts
            # check for awaiting messages
        except ValueError:
            raise InvalidRequestError()
        except LoginNotFoundError:
            response = Responses.LogInResponse.get_wrong_login_response()
        except PasswordError:
            response = Responses.LogInResponse.get_wrong_password_response()

        self.request.sendall(response)

    def handle_add_contact_request(self, add_contact_request):
        try:
            key = int.from_bytes(add_contact_request[:4], "big")
            contact_login = add_contact_request[5:].decode("utf-8", "replace")
            user = UserManager.get_online_user_by_key(key)
            DatabaseConnection().add_contact(user.login, contact_login)
            response = Responses.AddContactResponse.get_positive_response()
        except ValueError:
            raise InvalidRequestError()
        except ContactExistingError:
            # in theory the client side should prevent such travesty
            response = Responses.AddContactResponse.get_positive_response()
        except UserNotFoundError:
            response = Responses.AddContactResponse.get_user_not_found_response()

        self.request.sendall(response)

    def handle_get_contacts_request(self, get_contacts_request):
        try:
            key = int.from_bytes(get_contacts_request[:4], "big")
            user = UserManager.get_online_user_by_key(key)
            contacts = DatabaseConnection().get_contacts_list(user.login)
            if len(contacts) > 0:
                response = Responses.GetContacts.get_positive_response(contacts)
            else:
                response = Responses.GetContacts.get_no_contacts_response()
        except ValueError:
            raise InvalidRequestError()

        self.request.sendall(response)

    prefixes_to_methods = {
        0x00: handle_signup_request,
        0x01: handle_login_request,
        # 0x02: handle_logout_request,
        0x03: handle_get_contacts_request,
        0x04: handle_add_contact_request,
    }

    def handle(self):
        while True:
            try:
                data = self.request.recv(1024)
                if data:
                    prefix = data[0]
                    handler_method = self.prefixes_to_methods[prefix]
                    handler_method(self, data[1:])
            except (ConnectionResetError, ConnectionAbortedError):
                print("Zakończono połączenie.")
                break
