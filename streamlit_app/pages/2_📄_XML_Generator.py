"""
XML Message Generator
Example page demonstrating how to build features in the framework.
This page generates XML messages and allows downloading them.
"""

import streamlit as st
from streamlit_app.core import require_auth
from streamlit_app.components import render_footer
from streamlit_app.config.app_config import APP_CONFIG
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom


# Page configuration
st.set_page_config(
    page_title=f"XML Generator - {APP_CONFIG['app_name']}",
    page_icon="📄",
    layout="wide",
)

# Require authentication
if not require_auth():
    st.stop()


def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def generate_sample_xml(message_type, sender, receiver, content):
    """Generate a sample XML message."""
    # Create root element
    root = ET.Element("Message")
    
    # Add metadata
    metadata = ET.SubElement(root, "Metadata")
    ET.SubElement(metadata, "Type").text = message_type
    ET.SubElement(metadata, "Timestamp").text = datetime.now().isoformat()
    ET.SubElement(metadata, "Sender").text = sender
    ET.SubElement(metadata, "Receiver").text = receiver
    
    # Add content
    body = ET.SubElement(root, "Body")
    ET.SubElement(body, "Content").text = content
    
    return prettify_xml(root)


# Page content
st.title("📄 XML Message Generator")

st.markdown("""
Generate XML messages with custom parameters and download them.
This is a demonstration of how to build features using the framework.
""")

st.markdown("---")

# Input form
col1, col2 = st.columns(2)

with col1:
    message_type = st.selectbox(
        "Message Type",
        ["Order", "Invoice", "Notification", "Report", "Custom"]
    )
    
    sender = st.text_input("Sender", value=st.session_state.user['username'])

with col2:
    receiver = st.text_input("Receiver", placeholder="Enter receiver name")
    
    content = st.text_area(
        "Message Content",
        placeholder="Enter your message content here...",
        height=100
    )

# Generate button
if st.button("🔨 Generate XML", type="primary", use_container_width=True):
    if not receiver or not content:
        st.error("Please fill in all required fields (Receiver and Content)")
    else:
        # Generate XML
        xml_content = generate_sample_xml(message_type, sender, receiver, content)
        
        # Store in session state
        st.session_state['generated_xml'] = xml_content
        st.session_state['xml_filename'] = f"{message_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
        
        st.success("✅ XML generated successfully!")

# Display generated XML
if 'generated_xml' in st.session_state:
    st.markdown("---")
    st.subheader("Generated XML")
    
    # Show XML in code block
    st.code(st.session_state['generated_xml'], language='xml')
    
    # Download button
    st.download_button(
        label="⬇️ Download XML",
        data=st.session_state['generated_xml'],
        file_name=st.session_state['xml_filename'],
        mime="application/xml",
        use_container_width=True
    )
    
    # Option to save to database (example)
    if st.button("💾 Save to Database (Demo)", use_container_width=True):
        from streamlit_app.core import get_db_connection
        
        # This is just a demo - you'd need to create the table first
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Create table if it doesn't exist (add this to init_db.py in production)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS xml_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_by TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert the XML message
            cursor.execute(
                "INSERT INTO xml_messages (filename, content, created_by) VALUES (?, ?, ?)",
                (st.session_state['xml_filename'], st.session_state['generated_xml'], 
                 st.session_state.user['username'])
            )
            
            conn.commit()
            conn.close()
            
            st.success("✅ XML message saved to database!")
        except Exception as e:
            st.error(f"❌ Error saving to database: {e}")

# Show saved messages
with st.expander("📚 View Saved Messages"):
    from streamlit_app.core import get_db_connection
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT filename, created_by, created_at 
            FROM xml_messages 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        
        messages = cursor.fetchall()
        conn.close()
        
        if messages:
            st.write(f"Found {len(messages)} saved message(s):")
            for msg in messages:
                st.write(f"- **{msg['filename']}** by {msg['created_by']} at {msg['created_at']}")
        else:
            st.info("No saved messages yet. Generate and save one to get started!")
    except:
        st.info("No saved messages table yet. Save a message to create it.")

# Render footer
render_footer()
