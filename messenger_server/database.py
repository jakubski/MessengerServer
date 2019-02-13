import sqlite3


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


class DatabaseConnection:
    DBPATH = "database.db"

    def __init__(self):
        self._connection = sqlite3.connect(self.DBPATH)
        self._cursor = self._connection.cursor()

    def setup(self):
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
        try:
            self._cursor.execute("""SELECT login, password
                                    FROM users WHERE login=?""", (login, ))
            record = self._cursor.fetchone()
            if isinstance(record, type(None)):
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
