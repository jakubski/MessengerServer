from messenger_server.database import DatabaseConnection
from messenger_server.user_management import UserManager
from messenger_server.responses import Responses


class UserNotifier:
    """Class for sending packets that are not direct responses to incoming requests."""

    @staticmethod
    def notify_users_of_contact_login(contact):
        """Send status update to everyone who has the user in their contacts and is online.

        :param contact: User whose status was updated
        :type contact: :py:class:`messenger_server.user_management.OnlineUser`
        """
        users = DatabaseConnection().get_users_with_contact(contact.login)
        if users:
            notification = Responses.StatusUpdateNotification.get_status_update_notification(contact.login, 1)
            for user in users:
                online_user = UserManager.get_online_user_by_login(user)
                if online_user is not None:
                    online_user.socket.sendall(notification)

    @staticmethod
    def send_message(sender, recipient, message):
        """Send message to specified recipient.

        :param sender: Sender of the message
        :type sender: :py:class:`messenger_server.user_management.OnlineUser`
        :param recipient: Recipient of the message
        :type recipient: :py:class:`messenger_server.user_management.OnlineUser`
        :param message: Contents of the message
        :type message: str
        """
        notification = Responses.MessageNotification.get_message_notification(sender.login, message)
        recipient.socket.sendall(notification)
        # TODO: save to database
