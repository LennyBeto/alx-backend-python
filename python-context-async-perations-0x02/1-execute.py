import sqlite3

class ExecuteQuery:
    """
    A reusable context manager for executing parameterized SQL queries.
    Handles connection, execution, and cleanup automatically.
    """
    
    def __init__(self, db_path='users.db', query=None, params=None):
        """
        Initialize the context manager.
        
        Args:
            db_path (str): Path to SQLite database file
            query (str): SQL query with placeholders
            params (tuple): Parameters for the query
        """
        self.db_path = db_path
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """
        Enter the runtime context - opens connection and executes query.
        Returns self for result access.
        """
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        if self.query:
            self.cursor.execute(self.query, self.params or ())
            self.results = self.cursor.fetchall()
            
        return self

    def execute(self, query, params=None):
        """
        Execute additional queries within the same context.
        
        Args:
            query (str): SQL query to execute
            params (tuple): Query parameters
        Returns:
            list: Query results
        """
        if not self.cursor:
            raise RuntimeError("No active database connection")
            
        self.cursor.execute(query, params or ())
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context - handles cleanup.
        Commits if no exceptions, rolls back otherwise.
        """
        if self.cursor:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.cursor.close()
        
        if self.conn:
            self.conn.close()
            
        return False  # Propagate exceptions

    def fetch_results(self):
        """Get results from the most recent query"""
        if self.results is None:
            raise ValueError("No query has been executed yet")
        return self.results


# Usage example
if __name__ == "__main__":
    # Initialize with query and parameter
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)
    
    # Use as context manager
    with ExecuteQuery(query=query, params=param) as executor:
        results = executor.fetch_results()
        print(f"Found {len(results)} users over age 25:")
        for user in results:
            print(user)
        
        # Can execute additional queries in same context
        print("\nGetting count of active users:")
        count = executor.execute("SELECT COUNT(*) FROM users WHERE status = 'active'")
        print(f"Active users: {count[0][0]}")
