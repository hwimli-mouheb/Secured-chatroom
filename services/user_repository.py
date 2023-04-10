from db.user_db_connection import UserDbConnection


class UserRepository:
    @staticmethod
    def init_table():
        connection = UserDbConnection.get_instance()
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users
            (id_ text PRIMARY KEY, username text UNIQUE, salt text, password text, connected number)
        ''')
        return cursor

    @staticmethod
    def insert_user(user):
        cursor = UserRepository.init_table()
        cursor.execute(
            "INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?)",
            (user['id_'],  user['username'],
             user['salt'], user['password'], 0)
        )
        UserDbConnection.get_instance().commit()

    @staticmethod
    def get_by_username(username):
        cursor = UserRepository.init_table()
        cursor.execute(
            "SELECT password, salt FROM users WHERE username like ?",
            (username.decode(),)
        )
        return cursor.fetchone()

    @staticmethod
    def get_connected_users():
        cursor = UserRepository.init_table()
        cursor.execute("SELECT username FROM users WHERE connected = 1")
        return cursor.fetchall()

    @staticmethod
    def connect(username):
        cursor = UserRepository.init_table()
        cursor.execute(
            "UPDATE users set connected = 1 WHERE username LIKE ?", (username.decode(),))
        UserDbConnection.get_instance().commit()

    @staticmethod
    def disconnect(username):
        cursor = UserRepository.init_table()
        cursor = UserRepository.init_table()
        cursor.execute(
            "UPDATE users set connected = 0 WHERE username LIKE ?", (username.decode(),))
        UserDbConnection.get_instance().commit()
