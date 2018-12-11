import sqlite3


class LoginTakenError(Exception):
    pass


class DatabaseConnection:
    DBPATH = "database.db"

    def __init__(self):
        try:
            self._connection = sqlite3.connect(self.DBPATH)
            self._cursor = self._connection.cursor()
            self._cursor.execute("""CREATE TABLE IF NOT EXISTS 
                                    users(login TEXT PRIMARY KEY, email TEXT, password TEXT)""")
            self._connection.commit()
        except Exception as e:
            self._connection.rollback()
            raise e
        finally:
            self._connection.close()

    def add_user(self, email, login, password):
        try:
            self._connection = sqlite3.connect(self.DBPATH)
            self._cursor = self._connection.cursor()
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
