import os
import psycopg2
from contextlib import contextmanager

# You can configure these via environment variables or a local test database string
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "field_agent_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

@contextmanager
def get_db_connection():
    """Context manager for safe PostgreSQL database connections."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        yield conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise e
    finally:
        if conn:
            conn.close()

def init_db():
    """Initializes the tickets table if it doesn't already exist."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS field_tickets (
                        ticket_id VARCHAR(50) PRIMARY KEY,
                        worker_id VARCHAR(50),
                        action VARCHAR(100),
                        notes TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                conn.commit()
        print("Database table 'field_tickets' initialized successfully.")
    except Exception as e:
        print(f"Notice: Running in local simulation mode (DB not strictly required for test run): {e}")

def save_ticket_action(worker_id: str, intent_data: dict):
    """Saves or updates the processed intent data into the PostgreSQL database."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO field_tickets (ticket_id, worker_id, action, notes)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (ticket_id) 
                    DO UPDATE SET action = EXCLUDED.action, notes = EXCLUDED.notes, updated_at = CURRENT_TIMESTAMP;
                """, (
                    intent_data.get("ticket_id", "UNKNOWN"),
                    worker_id,
                    intent_data.get("action", "general_update"),
                    intent_data.get("notes", "")
                ))
                conn.commit()
        return True
    except Exception as e:
        print(f"Database write skipped/simulated due to missing local PostgreSQL server: {e}")
        return False