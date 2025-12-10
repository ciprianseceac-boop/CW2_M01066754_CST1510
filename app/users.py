import bcrypt

def hash_password(password: str) -> str:
    """Hash a password for storage."""        
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)    
    return hashed.decode('utf-8')

def verify_password(provided_password: str, stored_password: str) -> bool:
    """Verify a stored password against one provided by user"""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

def set_user(conn, name, hash):
    cur = conn.cursor()
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    cur.execute(sql, (name, hash))
    conn.commit()

def get_one_user(conn, name):
    cur = conn.cursor()
    sql = "SELECT id, username, password_hash FROM users WHERE username = ?"
    cur.execute(sql, (name,))
    return cur.fetchone()

def login_user(conn, name, password):
    user = get_one_user(conn, name)
    if not user:
        return False, "User not found."
    _, name_db, hash_db = user
    if verify_password(password, hash_db):
        return True, "Login successful."
    return False, "Login failed."

def get_all_users(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM users")
    users = cur.fetchall()
    if not users:
        print("No users found.")
    for user in users:
        print(user)

def delete_user(conn, name):
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = ?", (name,))
    conn.commit()
    print(f"User {name} deleted successfully.")

def update_user(conn, old_name, new_name):
    cur = conn.cursor()
    cur.execute("UPDATE users SET username = ? WHERE username = ?", (new_name, old_name))
    conn.commit()

def migrate_users(conn):
    with open('DATA\\users.txt', 'r') as f:
        for line in f:
            name, hash = line.strip().split(',')
            set_user(conn, name, hash)

def register_username(conn, name, password):
    try:
        hashed = hash_password(password)
        set_user(conn, name, hashed)
        return True, f"User '{name}' registered successfully."
    except Exception as e:
        return False, f"Registration failed: {str(e)}"
