import bcrypt
import sqlite3
from pathlib import Path


DATA_DIR = Path("DATA")
DATA_PATH = DATA_DIR / "intelligence_platform.db"

def create_user_table(conn):
    conn = sqlite3.connect(DATA_PATH)
    curr = conn.cursor()
    curr.execute(
        """ CREATE TABLE IF NOT EXISTS users ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
            )""" ) 
    conn.commit()
    print("User table created successfully.")

def register_username(conn):
    name = input("Enter new username: ").strip()
    password = input("Enter new password: ").strip()
    hashed = hash_password(password)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (name, hashed))
    conn.commit()
    print(f"User '{name}' registered successfully.")

def login_user(conn) -> bool:
    name = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    user = get_one_user(conn, name)
    if user:
        _, name_db, hash_db = user
        if verify_password(password, hash_db):   # <-- fixed here
            return True
    return False

def get_one_user(conn, name):
    curr = conn.cursor()
    sql = (""" SELECT * FROM users WHERE username = ?""")
    param = (name,)
    curr.execute(sql, param)
    user = curr.fetchone()
    return(user) 

def hash_password(password: str) -> str:
    """Hash a password for storage."""        
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)    
    return hashed.decode('utf-8')

def verify_password(provided_password: str, stored_password: str) -> bool:
    """Verify a stored password against one provided by user"""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))
    
def main():
    conn = sqlite3.connect(DATA_PATH)
    create_user_table(conn)
    print(" Welcome to the system!")
    while True:
        print("\nPlease choose an option:")
        print("1. Register a new user")
        print("2. Login with existing user")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == "1":
            register_username(conn)
            print("User registered successfully!")              
        elif choice == "2":
            if login_user(conn):
                print("Login successful!")
            else:
                print("Login failed. Invalid username or password.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()  