from app.Models.database import DataBaseManager


def add_modify_at_column(db, table):
    query = f"""
        ALTER TABLE {table} 
        ADD COLUMN modify_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    """
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    cursor.close()
    return True


def migrate_modify_at_data(db, table):
    query = f"""
        UPDATE {table} 
        SET modify_at = created_at
        WHERE modify_at IS NULL
    """
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    cursor.close()
    return True


def do_process():
    db = DataBaseManager().connect(use_database=True)

    for table in ['user_signup', 'user_password']:
        if add_modify_at_column(db, table):
            print(f"Column 'modify_at' added to {table}.")
        else:
            print(f"Failed to add 'modify_at' to {table}.")

        if migrate_modify_at_data(db, table):
            print(f"Data migrated successfully in {table}.")
        else:
            print(f"Data migration failed in {table}.")

    db.close()


if __name__ == "__main__":
    print("Starting Processing...")
    do_process()
    print("Processing Completed..!!")
