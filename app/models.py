"""
Object-Oriented Model for Cybersecurity Domain
SecurityIncident class with full CRUD and analytics capabilities
"""

import pandas as pd
from datetime import datetime


class SecurityIncident:
    """Represents a cybersecurity incident with CRUD operations"""
    
    def __init__(self, conn, incident_id=None):
        """
        Initialize SecurityIncident object
        
        Args:
            conn: Database connection
            incident_id: Unique incident identifier
        """
        self.conn = conn
        self.incident_id = incident_id
        self.timestamp = None
        self.severity = None
        self.category = None
        self.status = None
        self.description = None
    
    #  CREATE 
    
    def create(self, timestamp, severity, category, status, description):
        """
        Create a new security incident in the database
        
        Args:
            timestamp: When the incident occurred
            severity: Critical, High, Medium, or Low
            category: Type of incident (Phishing, Malware, etc.)
            status: Open, Resolved, or Closed
            description: Details about the incident
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if timestamp is None:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cur = self.conn.cursor()
            sql = """INSERT INTO cyber_incidents 
                     (incident_id, timestamp, severity, category, status, description) 
                     VALUES (?, ?, ?, ?, ?, ?)"""
            cur.execute(sql, (self.incident_id, timestamp, severity, category, status, description))
            self.conn.commit()
            
            # Update object attributes
            self.timestamp = timestamp
            self.severity = severity
            self.category = category
            self.status = status
            self.description = description
            
            return True
        except Exception as e:
            print(f"Error creating incident: {e}")
            return False
    
    #  READ 
    
    def load(self):
        """
        Load incident data from database by incident_id
        
        Returns:
            bool: True if found and loaded, False otherwise
        """
        sql = "SELECT * FROM cyber_incidents WHERE incident_id = ?"
        data = pd.read_sql(sql, self.conn, params=(self.incident_id,))
        
        if not data.empty:
            row = data.iloc[0]
            self.timestamp = row['timestamp']
            self.severity = row['severity']
            self.category = row['category']
            self.status = row['status']
            self.description = row['description']
            return True
        return False
    
    @staticmethod
    def get_all(conn):
        """
        Get all cyber incidents from database
        
        Args:
            conn: Database connection
            
        Returns:
            DataFrame: All incidents
        """
        sql = "SELECT * FROM cyber_incidents"
        return pd.read_sql(sql, conn)
    
    @staticmethod
    def get_by_severity(conn, severity):
        """
        Get incidents filtered by severity level
        
        Args:
            conn: Database connection
            severity: Critical, High, Medium, or Low
            
        Returns:
            DataFrame: Filtered incidents
        """
        sql = "SELECT * FROM cyber_incidents WHERE severity = ?"
        return pd.read_sql(sql, conn, params=(severity,))
    
    @staticmethod
    def get_by_category(conn, category):
        """
        Get incidents filtered by category
        
        Args:
            conn: Database connection
            category: Type of incident
            
        Returns:
            DataFrame: Filtered incidents
        """
        sql = "SELECT * FROM cyber_incidents WHERE category = ?"
        return pd.read_sql(sql, conn, params=(category,))
    
    # UPDATE 
    
    def update(self, severity=None, category=None, status=None, description=None):
        """
        Update incident attributes
        
        Args:
            severity: New severity level (optional)
            category: New category (optional)
            status: New status (optional)
            description: New description (optional)
            
        Returns:
            bool: True if updated, False otherwise
        """
        updates = []
        params = []
        
        if severity is not None:
            updates.append("severity = ?")
            params.append(severity)
            self.severity = severity
            
        if category is not None:
            updates.append("category = ?")
            params.append(category)
            self.category = category
            
        if status is not None:
            updates.append("status = ?")
            params.append(status)
            self.status = status
            
        if description is not None:
            updates.append("description = ?")
            params.append(description)
            self.description = description
        
        if not updates:
            return False
        
        params.append(self.incident_id)
        sql = f"UPDATE cyber_incidents SET {', '.join(updates)} WHERE incident_id = ?"
        
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        
        return cur.rowcount > 0
    
       # DELETE 
    
    def delete(self):
        """
        Delete this incident from database
        
        Returns:
            bool: True if deleted, False otherwise
        """
        cur = self.conn.cursor()
        sql = "DELETE FROM cyber_incidents WHERE incident_id = ?"
        cur.execute(sql, (self.incident_id,))
        self.conn.commit()
        return cur.rowcount > 0
    
       # ANALYTICS 
    
    @staticmethod
    def get_phishing_trend(conn):
        """
        Analyze phishing incidents over time
        
        Args:
            conn: Database connection
            
        Returns:
            DataFrame: Date and count of phishing incidents
        """
        sql = """SELECT DATE(timestamp) as date, 
                 COUNT(*) as phishing_count
                 FROM cyber_incidents 
                 WHERE category = 'Phishing'
                 GROUP BY DATE(timestamp)
                 ORDER BY date"""
        return pd.read_sql(sql, conn)
    
    @staticmethod
    def detect_phishing_spike(conn):
        """
        Detect if there's an unusual spike in phishing attacks
        
        Args:
            conn: Database connection
            
        Returns:
            dict: Analysis with spike detection and statistics
        """
        phishing_trend = SecurityIncident.get_phishing_trend(conn)
        
        if phishing_trend.empty:
            return {
                'spike_detected': False,
                'message': 'No phishing data available'
            }
        
        avg_count = phishing_trend['phishing_count'].mean()
        max_count = phishing_trend['phishing_count'].max()
        
        spike_detected = max_count > avg_count * 1.5
        
        return {
            'spike_detected': spike_detected,
            'average': avg_count,
            'peak': max_count,
            'message': f"Spike detected: Peak {int(max_count)} vs Average {avg_count:.1f}" if spike_detected else "Normal levels"
        }
    
    @staticmethod
    def get_severity_distribution(conn):
        """
        Get incident count by severity level
        
        Args:
            conn: Database connection
            
        Returns:
            DataFrame: Severity levels and counts
        """
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
    
    @staticmethod
    def get_category_breakdown(conn):
        """
        Get incident count by category with status breakdown
        
        Args:
            conn: Database connection
            
        Returns:
            DataFrame: Categories with open/resolved counts
        """
        sql = """SELECT category, COUNT(*) as count,
                 SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) as open_count,
                 SUM(CASE WHEN status = 'Resolved' THEN 1 ELSE 0 END) as resolved_count
                 FROM cyber_incidents 
                 GROUP BY category
                 ORDER BY count DESC"""
        return pd.read_sql(sql, conn)
    
    @staticmethod
    def get_open_incidents(conn):
        """
        Get all open incidents
        
        Args:
            conn: Database connection
            
        Returns:
            DataFrame: All open incidents
        """
        sql = "SELECT * FROM cyber_incidents WHERE status = 'Open'"
        return pd.read_sql(sql, conn)
    
    @staticmethod
    def get_critical_incidents(conn):
        """
        Get all critical severity incidents
        
        Args:
            conn: Database connection
            
        Returns:
            DataFrame: All critical incidents
        """
        sql = "SELECT * FROM cyber_incidents WHERE severity = 'Critical'"
        return pd.read_sql(sql, conn)
    
    # UTILITY METHODS
    
    def is_critical(self):
        """Check if this incident is critical severity"""
        return self.severity == 'Critical'
    
    def is_open(self):
        """Check if this incident is still open"""
        return self.status == 'Open'
    
    def resolve(self):
        """Mark this incident as resolved"""
        return self.update(status='Resolved')
    
    def close(self):
        """Mark this incident as closed"""
        return self.update(status='Closed')
    
    def __repr__(self):
        """String representation of the incident"""
        return f"SecurityIncident(id={self.incident_id}, severity='{self.severity}', category='{self.category}', status='{self.status}')"
    
    def __str__(self):
        """Human-readable string"""
        return f"Incident #{self.incident_id}: {self.severity} {self.category} - {self.status}"
