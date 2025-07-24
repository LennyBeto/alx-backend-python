import time
import sqlite3
import functools

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

def retry_on_failure(retries=3, delay=2):
    """Decorator to retry a function if it raises an exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < retries - 1:  # Check if there are more retries left
                        print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"All {retries} attempts failed.")
                        raise  # Re-raise the last exception
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### Attempt to fetch users with automatic retry on failure
try:
    users = fetch_users_with_retry()
    print(users)
except Exception as e:
    print(f"Failed to fetch users: {e}")
