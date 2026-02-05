"""
Main Application Entry Point
This is the main Streamlit app with login functionality.
"""

import streamlit as st
from streamlit_app.core import (
    init_session_state,
    authenticate_user,
    set_authenticated_user,
    clear_session,
    get_current_user,
)
from streamlit_app.components import render_footer
from streamlit_app.config.app_config import APP_CONFIG


# Page configuration
st.set_page_config(
    page_title=APP_CONFIG['app_name'],
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
init_session_state()


def render_login_form():
    """Render the login form in the sidebar."""
    st.sidebar.title("🔐 Login")
    
    with st.sidebar.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            user = authenticate_user(username, password)
            if user:
                set_authenticated_user(user)
                st.success(f"Welcome, {user['username']}!")
                st.rerun()
            else:
                st.error("Invalid username or password")


def render_user_info():
    """Render logged-in user information in the sidebar."""
    user = get_current_user()
    if user:
        st.sidebar.success(f"Logged in as: **{user['username']}**")
        st.sidebar.info(f"Role: **{user['role']}**")
        
        if st.sidebar.button("Logout", use_container_width=True):
            clear_session()
            st.rerun()


def main():
    """Main application logic."""
    
    # Sidebar: Login or User Info
    if not st.session_state.authenticated:
        render_login_form()
    else:
        render_user_info()
    
    # Main content
    st.title(f"🏠 {APP_CONFIG['app_name']}")
    
    if st.session_state.authenticated:
        st.success("✅ You are logged in!")
        
        st.markdown("---")
        
        st.header("Welcome to Your Streamlit App Framework")
        
        st.markdown("""
        This is your main application page. You can now:
        
        - ✅ Build your app features here
        - ✅ Add new pages in the `streamlit_app/pages/` directory
        - ✅ Access the database using `get_db_connection()`
        - ✅ Manage users (if you're an admin) via the sidebar
        
        ### Quick Start Guide
        
        1. **Add your app content** in this file (`streamlit_app/app.py`)
        2. **Create additional pages** by adding files to `streamlit_app/pages/` directory
        3. **Customize the footer** in `streamlit_app/config/app_config.py`
        4. **Add database tables** in `streamlit_app/scripts/init_db.py`
        
        ### Example: Using the Database
        
        ```python
        from streamlit_app.core import get_db_connection
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        ```
        
        ### Need Help?
        
        Check out the `README.md` file for detailed documentation!
        """)
        
        # Example of using the database
        with st.expander("📊 View All Users (Demo)"):
            from streamlit_app.core import get_all_users
            users = get_all_users()
            st.write(f"Total users: {len(users)}")
            for user in users:
                st.write(f"- {user['username']} ({user['role']})")
        
    else:
        st.info("👈 Please log in using the sidebar to access the application.")
        
        st.markdown("---")
        
        st.header("About This Framework")
        
        st.markdown("""
        This Streamlit Framework Template provides:
        
        - 🔐 **User Authentication**: Secure login/logout with password hashing
        - 👥 **User Management**: Admin interface to manage users
        - 💾 **SQLite Database**: Pre-configured database for your data
        - 🎨 **Configurable Footer**: Customizable footer component
        - 🚀 **Ready for Deployment**: Configured for Streamlit Cloud
        - ⚡ **uv-powered**: Fast dependency management
        
        ### First Time Setup
        
        The default admin credentials are:
        - **Username**: `admin`
        - **Password**: `changeme123`
        
        ⚠️ **Important**: Change the admin password after your first login!
        """)
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()
