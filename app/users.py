#usrs.py# User CRDUD
import sqlite3  
import pandas as pd

def add_user(conn, name, hash):
    curr = conn.cursor()
    sql = ("""INSERT INTO users (username, password_hash) VALUES (?, ?)""")
    param = (name, hash)
    curr.execute(sql, param)
    conn.commit()

def get_all_users(conn):
    curr = conn.cursor()
    sql = (""" SELECT * FROM users""")
    curr.execute(sql)
    users = curr.fetchall()
    conn.close()
    return users

def get_all_users_pandas(conn):
    conn = sqlite3.connect("DATA\\intelligence_platform.db")
    query = "SELECT * FROM USERS"
    df = pd.read_sql_query(query, conn)
    return(df)