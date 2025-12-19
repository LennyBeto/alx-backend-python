import sqlite3

class DatabaseConnection:
    """Class-based context manager for SQLite database connections"""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Enter the runtime context - opens connection and returns cursor"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the runtime context - closes connection and handles errors"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
        return False  

# Usage example
if __name__ == "__main__":
    try:
        with DatabaseConnection('users.db') as cursor:
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            print("Database Query Results:")
            for row in results:
                print(row)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
