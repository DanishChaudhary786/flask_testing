import mysql.connector
class DataBaseManager:
    def __init__(self, host="localhost", user='root', password = 'Danish786', database='Testing'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        return mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)

    def check_existing_user(self, email):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_signup WHERE email = %s", (email,))
        result = cursor.fetchall()
        return result

    def register_user(self,*kwargs):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO user_signup (name, email, password, created_at) VALUES (%s, %s, %s, %s)", kwargs)
        connection.commit()
        cursor.close()
        connection.close()
