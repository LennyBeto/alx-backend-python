import time
import sqlite3
import functools

# Global dictionary to cache query results
query_cache = {}

def with_db_connection(func):
    """Decorator to handle database connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open a database connection
        conn = sqlite3.connect('users.db')
        try:
            # Call the original function with the connection
            return func(conn, *args, **kwargs)
        finally:
            # Ensure the connection is closed after the function call
            conn.close()
    return wrapper

def cache_query(func):
    """Decorator to cache query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Check if the query result is already cached
        if query in query_cache:
            print("Using cached result for query:", query)
            return query_cache[query]
        
        # If not cached, call the original function
        result = func(conn, query, *args, **kwargs)
        
        # Cache the result
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print("First call results:", users)

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print("Second call results:", users_again)
