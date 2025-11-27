#create user table

def create_user_table(conn):
    curr = conn.cursor()
    curr.execute(
        """ CREATE TABLE IF NOT EXIST users ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
            )""" ) 
    conn.commit()
    print("User table created successfully.")