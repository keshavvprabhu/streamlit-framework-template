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

# Apply custom CSS theme (Portfolio Design)
custom_css = """
<style>
h1, h2, h3, h4, h5, h6 {
    color: #1A1F2E !important;
    font-weight: 600;
}

h1 {
    border-bottom: 3px solid #2B5A8C !important;
    padding-bottom: 0.75rem !important;
}

.stButton > button {
    background-color: #2B5A8C !important;
    color: white !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
}

.stButton > button:hover {
    background-color: #4A7BA7 !important;
    box-shadow: 0 4px 12px rgba(43, 90, 140, 0.3) !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

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
