import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv('local.env')


class DataBaseManager:
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASS')
        self.database = os.getenv('DB_DATABASE')

    def connect(self, use_database=True):
        """Forces MySQL to use TCP/IP instead of Named Pipes"""
        connection_params = {
            "host": self.host,
            "user": self.user,
            "password": self.password,
            "use_pure": True,  # Force Python Connector to use native implementation
        }
        if use_database:
            connection_params["database"] = self.database
        return mysql.connector.connect(**connection_params)

    def check_existing_user(self, email):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_signup WHERE email = %s", (email,))
        result = cursor.fetchall()
        return result

    def check_existing_user_for_authentication(self, email):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT password from user_password where user_id in \
        (SELECT id FROM user_signup WHERE email = %s)", (email,))
        return cursor.fetchall()

    def register_user(self, **kwargs):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            name = kwargs.get("name")
            email = kwargs.get("email")
            password = kwargs.get("password")
            created_at = kwargs.get("created_at")

            if not all([name, email, password, created_at]):
                raise ValueError("Missing required fields: name, email, password, created_at")
            cursor.execute(
                "INSERT INTO user_signup (name, email, created_at) VALUES (%s, %s, %s)",
                (name, email, created_at)
            )
            user_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO User_password (user_id, password, created_at) VALUES (%s, %s, %s)",
                (user_id, password, created_at)
            )
            connection.commit()

        except mysql.connector.Error as e:
            connection.rollback()
            print(f"❌ MySQL Error: {e}")

        except Exception as e:
            connection.rollback()
            print(f"❌ General Error: {e}")

        finally:
            cursor.close()
            connection.close()

    def check_existing_user_with_user_id(self, user_id):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_signup WHERE id = %s", (user_id,))
        result = cursor.fetchall()
        return result
