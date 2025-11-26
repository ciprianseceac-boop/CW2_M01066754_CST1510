#user_service.py Migration

import sqlite3
import pandas as pd
from app.users import add_user

def migrate_cyber_incidents(conn):
    data1 = pd.read_csv('DATA\\cyber_incidents.csv') 
    data1.to_sql( 'cyber_incidents', conn, if_exists='append', index=False ) 
    print("Data imported successfully.")



def migrate_user_data(conn):
    with open('DATA\\users.txt', 'r') as f:
        users = f.readlines()
    for user in users:
        name, hash = user.strip().split(',')
        add_user(conn, name, hash)  
conn = sqlite3.connect("DATA\\intelligence_platform.db") 
conn.close()

def migrate_it_tickets(conn):
    data1 = pd.read_csv('DATA\\it_tickets.csv') 
    data1.to_sql( 'it_tickets', conn, if_exists='append', index=False ) 
print("Data imported successfully.")
