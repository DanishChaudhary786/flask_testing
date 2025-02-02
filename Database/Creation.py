from app.Models.database import DataBaseManager
import os
from dotenv import load_dotenv

load_dotenv('local.env')


def database_creation(db):
    query = f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_DATABASE')}"
    db.cursor().execute(query)
    db.commit()
    return True


def user_signup_table(db):
    query = "CREATE TABLE IF NOT EXISTS user_signup (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password VARCHAR(255), created_at DATETIME)"
    db.cursor().execute(query)
    db.commit()
    return True


def do_process():
    db = DataBaseManager().connect(use_database=False)
    if database_creation(db):
        print("Database Created Successfully")
    else:
        print("Database Creation Failed")
        db.close()
        return
    db.close()
    db = DataBaseManager().connect(use_database=True)
    print("Starting Table Creation")
    if user_signup_table(db):
        print("User Sign-up Table Created Successfully")
    else:
        print("User Sign-up Table Creation Failed")

    db.close()


if __name__ == "__main__":
    print(f"Starting Processing...")
    do_process()
    print("Processing Completed..!!")
