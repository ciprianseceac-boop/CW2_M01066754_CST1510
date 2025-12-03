import pandas as pd

# ------- migrate tables -------

def migrate_cyber_incidents(conn):
    path = 'DATA\\cyber_incidents.csv'
    df = pd.read_csv(path)
    print(df.head())  # preview first rows
    df.to_sql('cyber_incidents', conn, if_exists='append', index=False)
    print("Cyber incidents imported successfully.")

def get_all_cyber_incidents(conn):
    sql = "SELECT * FROM cyber_incidents"
    data = pd.read_sql(sql, conn)
    return data
