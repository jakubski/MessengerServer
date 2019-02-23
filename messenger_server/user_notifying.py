import socketserver
from messenger_server.database import DatabaseConnection
from messenger_server.user_management import UserManager
from messenger_server.responses import Responses


class UserNotifier:
    @staticmethod
    def notify_users_of_contact_login(contact):
        users = DatabaseConnection().get_users_with_contact(contact.login)
        if len(users) > 0:
            notification = Responses.StatusUpdateNotification.get_status_update_notification(contact.login, 1)
            for user in users:
                online_user = UserManager.get_online_user_by_login(user)
                if online_user is not None:
                    online_user.socket.sendall(notification)
