"""
Authentication Module
Handles user authentication, password hashing, and session management.
"""

import bcrypt
import streamlit as st
from typing import Optional, Dict
from streamlit_app.core.database import get_db_connection


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password: Plain text password to verify
        password_hash: Hashed password to check against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """
    Authenticate a user with username and password.
    
    Args:
        username: User's username
        password: User's password
        
    Returns:
        Dict with user info if authenticated, None otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, username, password_hash, role FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user and verify_password(password, user['password_hash']):
        return {
            'id': user['id'],
            'username': user['username'],
            'role': user['role']
        }
    
    return None


def create_user(username: str, password: str, role: str = 'user') -> bool:
    """
    Create a new user.
    
    Args:
        username: Username for the new user
        password: Password for the new user
        role: User role ('admin' or 'user')
        
    Returns:
        bool: True if user created successfully, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False


def update_user_password(user_id: int, new_password: str) -> bool:
    """
    Update a user's password.
    
    Args:
        user_id: ID of the user
        new_password: New password
        
    Returns:
        bool: True if password updated successfully, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(new_password)
        
        cursor.execute(
            "UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (password_hash, user_id)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating password: {e}")
        return False


def delete_user(user_id: int) -> bool:
    """
    Delete a user.
    
    Args:
        user_id: ID of the user to delete
        
    Returns:
        bool: True if user deleted successfully, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False


def get_all_users():
    """
    Get all users (excluding password hashes).
    
    Returns:
        list: List of user dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, role, created_at FROM users ORDER BY username")
    users = cursor.fetchall()
    conn.close()
    
    return [dict(user) for user in users]


def is_admin(user: Dict) -> bool:
    """
    Check if a user has admin role.
    
    Args:
        user: User dictionary
        
    Returns:
        bool: True if user is admin, False otherwise
    """
    return user.get('role') == 'admin'


def require_auth() -> bool:
    """
    Require authentication for a page.
    Call this at the top of protected pages.
    
    Returns:
        bool: True if user is authenticated, False otherwise
    """
    if 'authenticated' not in st.session_state or not st.session_state.authenticated:
        st.warning("⚠️ Please log in to access this page.")
        st.info("👈 Use the login form in the sidebar.")
        return False
    return True


def require_admin() -> bool:
    """
    Require admin role for a page.
    Call this at the top of admin-only pages.
    
    Returns:
        bool: True if user is authenticated admin, False otherwise
    """
    if not require_auth():
        return False
    
    if not is_admin(st.session_state.user):
        st.error("❌ You don't have permission to access this page.")
        st.info("This page is only accessible to administrators.")
        return False
    
    return True


def logout():
    """Log out the current user."""
    for key in ['authenticated', 'user']:
        if key in st.session_state:
            del st.session_state[key]
