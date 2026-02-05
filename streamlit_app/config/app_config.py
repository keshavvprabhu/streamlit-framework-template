"""
Application Configuration
Customize these settings for your specific app.
"""

APP_CONFIG = {
    # App metadata
    "app_name": "Streamlit App Framework",
    "version": "1.0.0",
    
    # Footer configuration
    "copyright_year": "2024",
    "copyright_holder": "Your Organization",
    
    # Footer links - add or remove as needed
    "footer_links": [
        {"text": "Documentation", "url": "https://docs.streamlit.io"},
        {"text": "GitHub", "url": "https://github.com"},
        {"text": "Support", "url": "mailto:support@example.com"},
    ],
    
    # Database settings
    "db_path": "data/app.db",
    
    # Session settings
    "session_timeout_minutes": 60,
}
