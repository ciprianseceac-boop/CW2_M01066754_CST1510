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
    curr = conn.cursor()
    sql = ("""INSERT INTO users (user_name, password_hash) VALUES (?, ?)""")
    param = (name, hash)
    curr.execute(sql, param)
    conn.commit()

def get_one_user(conn, name):
    curr = conn.cursor()
    sql = (""" SELECT * FROM users WHERE username = ?""")
    param = (name,)
    curr.execute(sql, param)
    user = curr.fetchone()
    return(user) 

def login_user(conn):
    name = input("Enter name to login: ")
    password = input("Enter password to login: ")  
    id,name_db,hash_db = get_one_user(conn, name)
    if name == name_db:
        return verify_password(hash_db, password)
    return False

def get_all_users(conn):
    curr = conn.cursor()
    sql = (""" SELECT * FROM users""")
    curr.execute(sql)
    all_users = curr.fetchall()
    for i in all_users:
        print(i)
    
def delete_user(conn, name):
    curr = conn.cursor()
    sql = (""" DELETE FROM users WHERE user_name = ?""")
    param = (name,)
    curr.execute(sql, param)
    conn.commit()
    print(f"User {name} deleted successfully.")

def update_user(conn, old_name, new_name):
    curr = conn.cursor()
    sql = (""" UPDATE users SET user_name = ? WHERE user_name = ?""")
    param = (new_name, old_name)
    curr.execute(sql, param)
    conn.commit()
        
def migrate_users(conn):
    with open('DATA\\users.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        name, hash = line.strip().split(',')
        set_user(conn, name, hash)
    conn.close()

def register_username(conn):
    name = input("Enter new username: ").strip()
    password = input("Enter new password: ").strip()
    hashed = hash_password(password)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (name, hashed))
    conn.commit()
    print(f"User '{name}' registered successfully.")
