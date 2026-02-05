"""
Database Module
Handles SQLite database connection and operations.
"""

import sqlite3
import os
from typing import Optional
from config.app_config import APP_CONFIG


def get_db_path() -> str:
    """Get the database file path."""
    return APP_CONFIG["db_path"]


def ensure_data_directory():
    """Ensure the data directory exists."""
    db_path = get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)


def get_db_connection() -> sqlite3.Connection:
    """
    Get a connection to the SQLite database.
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    ensure_data_directory()
    db_path = get_db_path()
    
    # Enable foreign key constraints
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    
    # Return rows as dictionaries for easier access
    conn.row_factory = sqlite3.Row
    
    return conn


def init_database():
    """
    Initialize the database with required tables.
    This is called automatically on first run.
    """
    ensure_data_directory()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create an index on username for faster lookups
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_username ON users(username)
    """)
    
    # Add your custom tables here
    # Example:
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS your_table (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         name TEXT NOT NULL,
    #         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #     )
    # """)
    
    conn.commit()
    conn.close()


def database_exists() -> bool:
    """Check if the database file exists."""
    return os.path.exists(get_db_path())


# Auto-initialize database if it doesn't exist
if not database_exists():
    init_database()
