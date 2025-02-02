from app.Models.database import DataBaseManager


def password_table_creation(db):
    query = """
        CREATE TABLE IF NOT EXISTS user_password(
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES user_signup(id) ON DELETE CASCADE
            )
        """
    db.cursor().execute(query)
    db.commit()
    return True


def data_migration(db):
    query = """
        INSERT INTO user_password (user_id, password, created_at) 
        SELECT id, password, created_at FROM user_signup        
    """
    db.cursor().execute(query)
    db.commit()
    return True


def delete_password_column(db):
    query = "ALTER TABLE user_signup DROP COLUMN password"
    db.cursor().execute(query)
    db.commit()


def do_process():
    db = DataBaseManager().connect(use_database=True)
    if password_table_creation(db):
        print("Password Table Created Successfully")
    else:
        print("Password Table Creation Failed")

    if data_migration(db):
        print("Data Migrated Successfully")
    else:
        print("Data Migration Failed")

    if delete_password_column(db):
        print("Password Column Deleted Successfully")
    else:
        print("Password Column Deletion Failed")

    db.close()


if __name__ == "__main__":
    print(f"Starting Processing...")
    do_process()
    print("Processing Completed..!!")
