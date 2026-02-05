"""
Footer Component
Reusable footer for Streamlit apps.
"""

import streamlit as st
from streamlit_app.config.app_config import APP_CONFIG


def render_footer():
    """
    Render the application footer with copyright and links.
    Configure the footer content in streamlit_app/config/app_config.py
    """
    footer_html = f"""
    <style>
        .footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f0f2f6;
            color: #262730;
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
            border-top: 1px solid #e0e0e0;
            z-index: 999;
        }}
        .footer a {{
            color: #FF4B4B;
            text-decoration: none;
            margin: 0 10px;
        }}
        .footer a:hover {{
            text-decoration: underline;
        }}
        .footer-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
    </style>
    <div class="footer">
        <div class="footer-content">
            <span>© {APP_CONFIG['copyright_year']} {APP_CONFIG['copyright_holder']}</span>
            <span style="margin: 0 5px;">|</span>
            <span>v{APP_CONFIG['version']}</span>
    """
    
    # Add footer links
    if APP_CONFIG.get('footer_links'):
        footer_html += '<span style="margin: 0 5px;">|</span>'
        for i, link in enumerate(APP_CONFIG['footer_links']):
            footer_html += f'<a href="{link["url"]}" target="_blank">{link["text"]}</a>'
            if i < len(APP_CONFIG['footer_links']) - 1:
                footer_html += '<span style="margin: 0 5px;">•</span>'
    
    footer_html += """
        </div>
    </div>
    """
    
    st.markdown(footer_html, unsafe_allow_html=True)


def render_simple_footer(text: str):
    """
    Render a simple custom footer with just text.
    
    Args:
        text: Footer text to display
    """
    footer_html = f"""
    <style>
        .simple-footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f0f2f6;
            color: #262730;
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
            border-top: 1px solid #e0e0e0;
            z-index: 999;
        }}
    </style>
    <div class="simple-footer">
        {text}
    </div>
    """
    
    st.markdown(footer_html, unsafe_allow_html=True)
