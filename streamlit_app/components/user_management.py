"""
User Management Component
UI components for managing users (admin only).
"""

import streamlit as st
from streamlit_app.core.auth import create_user, get_all_users, delete_user, update_user_password


def render_user_creation_form():
    """Render form to create a new user."""
    st.subheader("Create New User")
    
    with st.form("create_user_form"):
        username = st.text_input("Username", max_chars=50)
        password = st.text_input("Password", type="password", max_chars=100)
        confirm_password = st.text_input("Confirm Password", type="password", max_chars=100)
        role = st.selectbox("Role", ["user", "admin"])
        
        submitted = st.form_submit_button("Create User")
        
        if submitted:
            # Validation
            if not username or not password:
                st.error("Username and password are required.")
                return
            
            if len(username) < 3:
                st.error("Username must be at least 3 characters long.")
                return
            
            if len(password) < 8:
                st.error("Password must be at least 8 characters long.")
                return
            
            if password != confirm_password:
                st.error("Passwords do not match.")
                return
            
            # Create user
            if create_user(username, password, role):
                st.success(f"✅ User '{username}' created successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to create user. Username may already exist.")


def render_user_list():
    """Render list of all users with management options."""
    st.subheader("Existing Users")
    
    users = get_all_users()
    
    if not users:
        st.info("No users found.")
        return
    
    for user in users:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        
        with col1:
            st.write(f"**{user['username']}**")
        
        with col2:
            badge_color = "🔴" if user['role'] == 'admin' else "🟢"
            st.write(f"{badge_color} {user['role']}")
        
        with col3:
            st.write(f"ID: {user['id']}")
        
        with col4:
            # Don't allow deleting yourself
            current_user = st.session_state.get('user', {})
            if user['id'] != current_user.get('id'):
                if st.button("🗑️ Delete", key=f"delete_{user['id']}"):
                    if delete_user(user['id']):
                        st.success(f"User '{user['username']}' deleted.")
                        st.rerun()
                    else:
                        st.error("Failed to delete user.")
            else:
                st.write("_(You)_")
        
        st.divider()


def render_password_change_form():
    """Render form to change current user's password."""
    st.subheader("Change Your Password")
    
    with st.form("change_password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_new_password = st.text_input("Confirm New Password", type="password")
        
        submitted = st.form_submit_button("Change Password")
        
        if submitted:
            from streamlit_app.core.auth import authenticate_user
            
            current_user = st.session_state.get('user')
            if not current_user:
                st.error("Session expired. Please log in again.")
                return
            
            # Verify current password
            if not authenticate_user(current_user['username'], current_password):
                st.error("Current password is incorrect.")
                return
            
            # Validate new password
            if len(new_password) < 8:
                st.error("New password must be at least 8 characters long.")
                return
            
            if new_password != confirm_new_password:
                st.error("New passwords do not match.")
                return
            
            # Update password
            if update_user_password(current_user['id'], new_password):
                st.success("✅ Password changed successfully!")
            else:
                st.error("❌ Failed to change password.")
