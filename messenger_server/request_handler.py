import socketserver
from threading import Thread
from messenger_server.database import *
from messenger_server.user_management import UserManager
from messenger_server.user_notifying import UserNotifier
from messenger_server.responses import Responses
from messenger_server.config import *


class InvalidRequestError(Exception):
    pass


class RequestHandler(socketserver.BaseRequestHandler):
    """Class used to handle each TCP request.

    As required by :py:class:`socketserver.BaseServer` this class inherits
    from :py:class:`socketserver.BaseRequestHandler` and is provided
    to the :py:class:`socketserver.TCPServer` to be instantiated for every
    incoming request and call the :py:func:`handle` function.

    :param request: a socket created by the request
    :type request: :py:class:`socket.socket`
    :param prefixes_to_methods: mapping of requests' prefixes to appropriate handling methods
    :type prefixes_to_methods: dict(int, function)
    """

    def handle_signup_request(self, signup_request):
        """Perform user sign-up and send adequate response.

        :param signup_request: Sign-up request without the prefix
        :type signup_request: bytes
        """
        try:
            email, login, password = signup_request.decode(ENCODING, "replace").split(DELIMITER_STR)
            DatabaseConnection().add_user(email, login, password)
            response = Responses.SignUpResponse.get_positive_response()
        except ValueError:
            raise InvalidRequestError()
        except LoginTakenError:
            response = Responses.SignUpResponse.get_existing_login_response()

        self.request.sendall(response)

    def handle_login_request(self, login_request):
        """Perform user log-in and send adequate response.

        :param login_request: Log-in request without the prefix
        :type login_request: bytes
        """
        try:
            login, password = login_request.decode(ENCODING, "replace").split(DELIMITER_STR)
            DatabaseConnection().verify_login(login, password)
            user = UserManager.sign_in(login, self.request)
            response = Responses.LogInResponse.get_positive_response(user.key)

            notifier_thread_1 = Thread(target=UserNotifier.notify_users_of_contact_login, args=(user,))
            notifier_thread_1.start()
            # TODO: check for awaiting messages
        except ValueError:
            raise InvalidRequestError()
        except LoginNotFoundError:
            response = Responses.LogInResponse.get_wrong_login_response()
        except PasswordError:
            response = Responses.LogInResponse.get_wrong_password_response()

        self.request.sendall(response)

    def handle_add_contact_request(self, add_contact_request):
        """Perform adding user's contact and send adequate response.

        :param add_contact_request: Add-contact request without the prefix
        :type add_contact_request: bytes
        """
        try:
            key = int.from_bytes(add_contact_request[:4], ENDIANNESS)
            contact = add_contact_request[5:].decode(ENCODING, "replace")
            user = UserManager.get_online_user_by_key(key)
            DatabaseConnection().add_contact(user.login, contact)
            status = int(UserManager.get_online_user_by_login(contact) is not None)
            response = Responses.AddContactResponse.get_positive_response(status)
        except ValueError:
            raise InvalidRequestError()
        except ContactExistingError:
            # ideally the client side should prevent such possibility
            response = Responses.AddContactResponse.get_positive_response(status)
        except UserNotFoundError:
            response = Responses.AddContactResponse.get_user_not_found_response()

        self.request.sendall(response)

    def handle_get_contacts_request(self, get_contacts_request):
        """Perform fetching user's contact list and send adequate response.

        :param get_contacts_request: Get-contacts request without the prefix
        :type get_contacts_request: bytes
        """
        try:
            key = int.from_bytes(get_contacts_request[:4], ENDIANNESS)
            user = UserManager.get_online_user_by_key(key)
            contacts = DatabaseConnection().get_contacts_list(user.login)
            if contacts:
                contacts_with_statuses = \
                    [(c, int(UserManager.get_online_user_by_login(c) is not None)) for c in contacts]
                response = Responses.GetContacts.get_positive_response(contacts_with_statuses)
            else:
                response = Responses.GetContacts.get_no_contacts_response()
        except ValueError:
            raise InvalidRequestError()

        self.request.sendall(response)

    def handle_incoming_message(self, incoming_message_request):
        """Perform passing a message to another user and other adequate actions.

        :param incoming_message_request: Incoming message without the prefix
        :type incoming_message_request: bytes
        """
        try:
            key_b, contact_b, message_b = incoming_message_request.split(DELIMITER)
            key = int.from_bytes(key_b, ENDIANNESS)
            contact_login = contact_b.decode(ENCODING, "replace")
            message = message_b.decode(ENCODING, "replace")
            user = UserManager.get_online_user_by_key(key)
            contact = UserManager.get_online_user_by_login(contact_login)
            if contact is not None:
                UserNotifier.send_message(user, contact, message)
            # TODO: store in database
        except ValueError:
            raise InvalidRequestError()

    prefixes_to_methods = {
        0x00: handle_signup_request,
        0x01: handle_login_request,
        # 0x02: handle_logout_request,
        0x03: handle_get_contacts_request,
        0x04: handle_add_contact_request,
        0x06: handle_incoming_message,
    }

    def handle(self):
        """Retrieve incoming data and execute adequate handler function.

        When data has been received from the socket, the first byte is used
        to determine the type of the request, in accordance with the protocol.
        Corresponding method is then passed the received data minus the first byte.
        """
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
