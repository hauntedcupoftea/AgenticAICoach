import sqlite3
import os

# Set the database path inside the 'db' folder of the current package
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(PACKAGE_DIR, "db")
os.makedirs(DB_DIR, exist_ok=True)  # Ensure the 'db' folder exists
DB_PATH = os.path.join(DB_DIR, "cv_coach.db")


def init_db():
    """Initialize SQLite database with necessary tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cv_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            content BLOB NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cv_id INTEGER NOT NULL,
            user_message TEXT,
            assistant_message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cv_id) REFERENCES cv_files (id)
        );
        """
    )
    conn.commit()
    conn.close()


def save_cv_to_db(file):
    """Save uploaded CV to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO cv_files (filename, content) VALUES (?, ?)
    """,
        (file.name, file.read()),
    )
    conn.commit()
    conn.close()


def get_all_cvs():
    """Retrieve all uploaded CVs from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, filename, uploaded_at FROM cv_files ORDER BY uploaded_at DESC"
    )
    files = cursor.fetchall()
    conn.close()
    return files


def get_cv_content(cv_id):
    """Retrieve CV content by ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM cv_files WHERE id = ?", (cv_id,))
    content = cursor.fetchone()
    conn.close()
    return content[0] if content else None


def save_chat_to_db(cv_id, user_message, assistant_message):
    """Save chat messages associated with a specific CV."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO chat_history (cv_id, user_message, assistant_message)
            VALUES (?, ?, ?);
            """,
            (cv_id, user_message, assistant_message),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error saving chat: {e}")
    finally:
        conn.close()


def get_chat_history(cv_id):
    """Retrieve chat history for a specific CV."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT user_message, assistant_message, timestamp 
        FROM chat_history 
        WHERE cv_id = ?
        ORDER BY timestamp;
        """,
        (cv_id,),
    )
    history = cursor.fetchall()
    conn.close()
    return history
