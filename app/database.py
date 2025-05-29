import mysql.connector
from app.config import settings

def get_database_connection():
    """Create and return a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host=settings.DATABASE_HOST,
            user=settings.DATABASE_USER,
            password=settings.DATABASE_PASSWORD,
            database=settings.DATABASE_NAME,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error on connecting to the database: {err}")
        raise