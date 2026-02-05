#!/usr/bin/env python3
"""
Database Initialization Script
Run this script to initialize the database and create the default admin user.
"""

import sys
import os

from streamlit_app.core.database import init_database, get_db_connection
from streamlit_app.core.auth import create_user


def main():
    """Initialize the database and create default admin user."""
    print("Initializing database...")
    
    # Initialize database tables
    init_database()
    print("✅ Database tables created successfully!")
    
    # Check if admin user already exists
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE username = 'admin'")
    result = cursor.fetchone()
    conn.close()
    
    if result['count'] > 0:
        print("ℹ️  Admin user already exists. Skipping creation.")
        print("\nDatabase initialization complete!")
        return
    
    # Create default admin user
    print("\nCreating default admin user...")
    username = "admin"
    password = "changeme123"
    
    if create_user(username, password, "admin"):
        print(f"✅ Admin user created successfully!")
        print(f"\n📝 Default credentials:")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        print(f"\n⚠️  IMPORTANT: Change this password immediately after first login!")
    else:
        print("❌ Failed to create admin user.")
        sys.exit(1)
    
    print("\n✨ Database initialization complete!")
    print("\nYou can now run your Streamlit app with:")
    print("   uv run streamlit run streamlit_app/app.py")
    print("   or")
    print("   streamlit run streamlit_app/app.py")


if __name__ == "__main__":
    main()
