#schema.py# CREATE TABLE

def create_user_table(conn):
    curr = conn.cursor()
    sql = ("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL
    )""")
    curr.execute(sql)
    conn.commit()