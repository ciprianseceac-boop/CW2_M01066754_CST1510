import sqlite3
import pandas as pd

def migrate_datasets_metadata(conn):
    path = 'DATA\\datasets_metadata.csv'
    df = pd.read_csv(path) 
    print(df.head())  
    df.to_sql('datasets_metadata', conn, if_exists='append', index=False) 
    print("Datasets metadata imported successfully.")

def migrate_it_tickets(conn):
    path = 'DATA\\it_tickets.csv'
    df = pd.read_csv(path) 
    print(df.head())  
    df.to_sql('it_tickets', conn, if_exists='append', index=False) 
    print("IT tickets imported successfully.")

def migrate_user_data(conn):
    with open('DATA\\users.txt', 'r') as f:
        users = f.readlines()
    cur = conn.cursor()
    for user in users:
        name, hash = user.strip().split(',')
        cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (name, hash))
    conn.commit()
    print("User data imported successfully.")
