import pandas as pd
from datetime import datetime

#  MIGRATE/READ 

def migrate_cyber_incidents(conn):
    """Import cyber incidents from CSV into database"""
    path = 'DATA\\cyber_incidents.csv'
    df = pd.read_csv(path)
    print(df.head()) 
    df.to_sql('cyber_incidents', conn, if_exists='append', index=False)
    print("Cyber incidents imported successfully.")

def get_all_cyber_incidents(conn):
    """Retrieve all cyber incidents from database"""
    sql = "SELECT * FROM cyber_incidents"
    data = pd.read_sql(sql, conn)
    return data

def get_incident_by_id(conn, incident_id):
    """Get a single incident by ID"""
    sql = "SELECT * FROM cyber_incidents WHERE incident_id = ?"
    data = pd.read_sql(sql, conn, params=(incident_id,))
    return data

#  CREATE 

def create_cyber_incident(conn, incident_id, timestamp, severity, category, status, description):
    """Create a new cyber incident"""
    if timestamp is None:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cur = conn.cursor()
    sql = """INSERT INTO cyber_incidents 
             (incident_id, timestamp, severity, category, status, description) 
             VALUES (?, ?, ?, ?, ?, ?)"""
    cur.execute(sql, (incident_id, timestamp, severity, category, status, description))
    conn.commit()
    return True

#  UPDATE 

def update_cyber_incident(conn, incident_id, severity=None, category=None, status=None, description=None):
    """Update an existing cyber incident"""
    cur = conn.cursor()
    
    # Build dynamic update query
    updates = []
    params = []
    
    if severity is not None:
        updates.append("severity = ?")
        params.append(severity)
    if category is not None:
        updates.append("category = ?")
        params.append(category)
    if status is not None:
        updates.append("status = ?")
        params.append(status)
    if description is not None:
        updates.append("description = ?")
        params.append(description)
    
    if not updates:
        return False
    
    params.append(incident_id)
    sql = f"UPDATE cyber_incidents SET {', '.join(updates)} WHERE incident_id = ?"
    cur.execute(sql, params)
    conn.commit()
    return cur.rowcount > 0

#     DELETE

def delete_cyber_incident(conn, incident_id):
    """Delete a cyber incident by ID"""
    cur = conn.cursor()
    sql = "DELETE FROM cyber_incidents WHERE incident_id = ?"
    cur.execute(sql, (incident_id,))
    conn.commit()
    return cur.rowcount > 0

#  ANALYTICS 

def get_phishing_trend(conn):
    """Analyze phishing incidents over time"""
    sql = """SELECT DATE(timestamp) as date, 
             COUNT(*) as phishing_count
             FROM cyber_incidents 
             WHERE category = 'Phishing'
             GROUP BY DATE(timestamp)
             ORDER BY date"""
    return pd.read_sql(sql, conn)

def get_severity_distribution(conn):
    """Get incident count by severity"""
    sql = """SELECT severity, COUNT(*) as count 
             FROM cyber_incidents 
             GROUP BY severity 
             ORDER BY 
                CASE severity 
                    WHEN 'Critical' THEN 1
                    WHEN 'High' THEN 2
                    WHEN 'Medium' THEN 3
                    WHEN 'Low' THEN 4
                END"""
    return pd.read_sql(sql, conn)

def get_category_breakdown(conn):
    """Get incident count by category"""
    sql = """SELECT category, COUNT(*) as count,
             SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) as open_count,
             SUM(CASE WHEN status = 'Resolved' THEN 1 ELSE 0 END) as resolved_count
             FROM cyber_incidents 
             GROUP BY category
             ORDER BY count DESC"""
    return pd.read_sql(sql, conn)
