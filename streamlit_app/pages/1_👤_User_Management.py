"""
User Management Page
Admin-only page for managing users.
"""

import streamlit as st
from streamlit_app.core import require_admin
from streamlit_app.components import (
    render_footer,
    render_user_creation_form,
    render_user_list,
    render_password_change_form,
)
from streamlit_app.config.app_config import APP_CONFIG


# Page configuration
st.set_page_config(
    page_title=f"User Management - {APP_CONFIG['app_name']}",
    page_icon="👤",
    layout="wide",
)

# Require admin authentication
if not require_admin():
    st.stop()

# Page content
st.title("👤 User Management")

st.markdown("""
Manage user accounts for this application. You can create new users, 
view existing users, and delete users as needed.
""")

st.markdown("---")

# Create tabs for different management functions
tab1, tab2, tab3 = st.tabs(["Create User", "Manage Users", "Change Password"])

with tab1:
    render_user_creation_form()

with tab2:
    render_user_list()

with tab3:
    render_password_change_form()

# Render footer
render_footer()
