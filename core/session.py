"""
Session Management Module
Handles Streamlit session state for authentication.
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, Dict
from config.app_config import APP_CONFIG


def init_session_state():
    """Initialize session state variables."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    if 'login_time' not in st.session_state:
        st.session_state.login_time = None


def set_authenticated_user(user: Dict):
    """
    Set the authenticated user in session state.
    
    Args:
        user: User dictionary with id, username, and role
    """
    st.session_state.authenticated = True
    st.session_state.user = user
    st.session_state.login_time = datetime.now()


def clear_session():
    """Clear all session state."""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.login_time = None


def is_session_valid() -> bool:
    """
    Check if the current session is still valid.
    
    Returns:
        bool: True if session is valid, False otherwise
    """
    if not st.session_state.authenticated or not st.session_state.login_time:
        return False
    
    timeout_minutes = APP_CONFIG.get('session_timeout_minutes', 60)
    timeout_delta = timedelta(minutes=timeout_minutes)
    
    if datetime.now() - st.session_state.login_time > timeout_delta:
        clear_session()
        return False
    
    return True


def get_current_user() -> Optional[Dict]:
    """
    Get the currently authenticated user.
    
    Returns:
        Dict with user info if authenticated, None otherwise
    """
    if is_session_valid():
        return st.session_state.user
    return None
