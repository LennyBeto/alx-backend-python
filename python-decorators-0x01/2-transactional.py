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

def transactional(func):
    """Decorator to manage database transactions."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Execute the original function
            result = func(conn, *args, **kwargs)
            # Commit the transaction if successful
            conn.commit()
            return result
        except Exception as e:
            # Rollback the transaction in case of an error
            conn.rollback()
            print(f"Transaction failed: {e}")
            raise  # Re-raise the exception for further handling
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

#### Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
