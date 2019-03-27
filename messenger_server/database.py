import sqlite3
from messenger_server.config import DBPATH


class LoginTakenError(Exception):
    pass

class LoginNotFoundError(Exception):
    pass

class PasswordError(Exception):
    pass

class ContactExistingError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class NoContactsError(Exception):
    pass


class DatabaseConnection:
    """Single SQLite3 Database connection.

    :param _connection: Connection object for the database
    :type _connection: :py:class:`sqlite3.Connection`
    :param _cursor: Cursor object returned by _connection
    :type _cursor: :py:class:`sqlite3.Cursor`
    """
    def __init__(self):
        self._connection = sqlite3.connect(DBPATH)
        self._cursor = self._connection.cursor()
        self._cursor.execute("""PRAGMA foreign_keys=on""")

    def setup(self):
        """Prepare initial database structure in case it doesn't exist yet.

        This method should be called once before starting the server.
        """
        try:
            self._cursor.execute("""PRAGMA foreign_keys=on""")
            self._cursor.execute("""CREATE TABLE IF NOT EXISTS
                              users(login TEXT PRIMARY KEY, email TEXT, password TEXT)""")
            self._cursor.execute("""CREATE TABLE IF NOT EXISTS
                              contacts(user TEXT, contact TEXT,
                                       PRIMARY KEY (user, contact),
                                       FOREIGN KEY (contact) REFERENCES users(login))""")
            self._connection.commit()
        except Exception as e:
            self._connection.rollback()
            raise e
        finally:
            self._connection.close()

    def add_user(self, email, login, password):
        """Insert a record representing a single user.

        :param email: User's email address
        :type email: str
        :param login: User's login
        :type login: str
        :param password: User's password
        :type password: str
        :raises: :py:exc:`messenger_server.database.LoginTakenError`
                 if a record with identical login already exists
        """
        try:
            self._cursor.execute("""INSERT INTO users(login, email, password)
                                    values(?, ?, ?)""", (login, email, password))
            self._connection.commit()
        except Exception as e:
            self._connection.rollback()
            if isinstance(e, sqlite3.IntegrityError):
                raise LoginTakenError()
            else:
                raise e
        finally:
            self._connection.close()

    def verify_login(self, login, password):
        """Verify if given login matches given password in the database.

        :param login: Login being matched
        :type login: str
        :param password: Password being matched
        :type password: str
        :raises: :py:exc:`messenger_server.database.LoginNotFoundError`
                 if there is no record with given login
        :raises: :py:exc:`messenger_server.database.PasswordError`
                 if password retrieved from the database does not match the password provided
        """
        try:
            self._cursor.execute("""SELECT login, password
                                    FROM users WHERE login=?""", (login, ))
            record = self._cursor.fetchone()
            if record is None:
                raise LoginNotFoundError()
            else:
                _login, _password = record
                if _password != password:
                    raise PasswordError()
        except Exception as e:
            self._connection.rollback()
            raise e
        finally:
            self._connection.close()

    def add_contact(self, user, contact):
        """Insert a record representing a (user, contact) pair.

        :param user: Login of user who is adding a new contact
        :type user: str
        :param contact: Login of user who is being added as contact
        :type contact: str
        :raises: :py:exc:`messenger_server.database.ContactExistingError`
                 if such pair already exists in the database
        :raises: :py:exc:`messenger_server.database.UserNotFoundError`
                 if contact does not exist in the users table
        """
        try:
            self._cursor.execute("""INSERT INTO contacts(user, contact)
                                    values(?, ?)""", (user, contact))
            self._connection.commit()
        except Exception as e:
            self._connection.rollback()
            if isinstance(e, sqlite3.IntegrityError):
                if "UNIQUE" in str(e):
                    raise ContactExistingError()
                elif "FOREIGN KEY" in str(e):
                    raise UserNotFoundError()
            else:
                raise e
        finally:
            self._connection.close()

    def get_contacts_list(self, user):
        """Get a list of given user's contacts.

        :param user: Login of user whose contacts are being retrieved
        :type user: str
        :return: a list of logins
        :rtype: list(str)
        """
        self._cursor.execute("""SELECT contact FROM contacts
                                WHERE user=?""", (user, ))
        contacts = self._cursor.fetchall()
        self._connection.close()

        return [c[0] for c in contacts]

    def get_users_with_contact(self, contact):
        """Get a list of users who have given contact.

        :param contact: Login of user being searched as a contact
        :type contact: str
        :return: a list of logins
        :rtype: list(str)
        """
        self._cursor.execute("""SELECT user FROM contacts
                                WHERE contact=?""", (contact,))
        users = self._cursor.fetchall()
        self._connection.close()

        return [u[0] for u in users]
