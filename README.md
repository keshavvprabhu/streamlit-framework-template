# Streamlit App Framework Template

A reusable template for building Streamlit applications with built-in authentication, user management, and SQLite database support. Now powered by **uv** for blazing-fast dependency management!

## Features

- 🔐 **Authentication System**: Session-based login/logout with password hashing
- 👥 **User Management**: Admin interface to create, update, and delete users
- 💾 **SQLite Database**: Pre-configured database with user management
- 🎨 **Configurable Footer**: Customizable footer component with copyright, links, and version info
- 🚀 **Ready for Streamlit Cloud**: Configured for free deployment
- ⚡ **uv-powered**: Fast, reliable dependency management with uv

## Quick Start with uv

### Prerequisites

Install [uv](https://github.com/astral-sh/uv):

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### 1. Clone this template
```bash
git clone <your-repo-url>
cd streamlit-framework-template
```

### 2. Setup with uv (One Command!)
```bash
# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package in editable mode with dependencies
uv pip install -e .
```

### 3. Initialize the database
```bash
# Using the installed script
init-db

# Or run directly
uv run python -m streamlit_app.scripts.init_db
```

This creates the SQLite database and an initial admin user:
- **Username**: `admin`
- **Password**: `changeme123`

⚠️ **IMPORTANT**: Change the admin password immediately after first login!

### 4. Run the app
```bash
# Using streamlit directly
uv run streamlit run streamlit_app/app.py

# Or if you have streamlit in your PATH
streamlit run streamlit_app/app.py
```

### 5. Deploy to Streamlit Cloud (Free)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set the main file path to: `streamlit_app/app.py`
5. Deploy!

## Alternative: Quick Setup with uv run

You can also use `uv run` for a completely isolated environment:

```bash
# Initialize database
uv run init-db

# Run the app
uv run streamlit run streamlit_app/app.py
```

## Project Structure

```
streamlit-framework-template/
├── pyproject.toml                  # uv/pip configuration
├── README.md                       # This file
├── .python-version                 # Python version specification
│
├── streamlit_app/                  # Main package
│   ├── __init__.py
│   ├── app.py                     # Application entry point
│   ├── cli.py                     # CLI commands
│   │
│   ├── core/                      # Business logic
│   │   ├── __init__.py
│   │   ├── auth.py               # Authentication
│   │   ├── database.py           # Database operations
│   │   └── session.py            # Session management
│   │
│   ├── components/                # Reusable UI
│   │   ├── __init__.py
│   │   ├── footer.py             # Footer component
│   │   └── user_management.py   # User management UI
│   │
│   ├── config/                    # Configuration
│   │   ├── __init__.py
│   │   └── app_config.py         # App settings
│   │
│   ├── pages/                     # Multi-page app
│   │   ├── 1_👤_User_Management.py
│   │   └── 2_📄_XML_Generator.py
│   │
│   ├── scripts/                   # Utility scripts
│   │   ├── __init__.py
│   │   └── init_db.py            # Database initialization
│   │
│   └── .streamlit/                # Streamlit config
│       └── config.toml           # Theme & settings
│
├── data/                          # Database storage
│   └── .gitkeep                  # (app.db created here)
│
└── tests/                         # Test suite (optional)
    └── __init__.py
```

## Configuration

### App Configuration (`streamlit_app/config/app_config.py`)

Customize your app's footer and metadata:

```python
APP_CONFIG = {
    "app_name": "My Streamlit App",
    "version": "1.0.0",
    "copyright_year": "2024",
    "copyright_holder": "Your Organization",
    "footer_links": [
        {"text": "Documentation", "url": "https://example.com/docs"},
        {"text": "Support", "url": "https://example.com/support"},
    ]
}
```

### Python Version

Specify your Python version in `.python-version`:
```
3.11
```

uv will automatically use this version when creating virtual environments.

## Usage

### Adding Authentication to Your Pages

```python
import streamlit as st
from streamlit_app.core.auth import require_auth

# Protect your page with authentication
if not require_auth():
    st.stop()

# Your page content here
st.title("Protected Page")
st.write("Only authenticated users can see this!")
```

### Using the Database

```python
from streamlit_app.core.database import get_db_connection

# Get a database connection
conn = get_db_connection()
cursor = conn.cursor()

# Execute queries
cursor.execute("SELECT * FROM your_table")
results = cursor.fetchall()

conn.close()
```

### Adding Custom Database Tables

Edit `streamlit_app/scripts/init_db.py` to add your own tables:

```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS your_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
```

## Development with uv

### Install Development Dependencies

```bash
uv pip install -e ".[dev]"
```

This installs additional tools:
- **pytest**: Testing framework
- **black**: Code formatter
- **ruff**: Fast linter

### Run Tests

```bash
uv run pytest
```

### Format Code

```bash
uv run black streamlit_app/
```

### Lint Code

```bash
uv run ruff check streamlit_app/
```

### Update Dependencies

```bash
# Update all dependencies to latest versions
uv pip install --upgrade -e .

# Update specific package
uv pip install --upgrade streamlit
```

### Add New Dependencies

Edit `pyproject.toml`:

```toml
dependencies = [
    "streamlit>=1.31.0",
    "bcrypt>=4.1.2",
    "pandas>=2.0.0",  # Add your new dependency
]
```

Then run:
```bash
uv pip install -e .
```

## User Management

### Creating Users

1. Log in as admin
2. Navigate to "User Management" in the sidebar
3. Fill in the user creation form
4. Click "Create User"

### Roles

Currently supports two roles:
- **admin**: Full access including user management
- **user**: Standard access (no user management)

## Security Best Practices

1. **Change default admin password immediately**
2. **Use strong passwords** for all accounts
3. **Don't commit the database** to version control (it's in `.gitignore`)
4. **Use environment variables** for sensitive configuration in production
5. **Enable HTTPS** when deploying (Streamlit Cloud does this automatically)

## Deployment to Streamlit Cloud

### Option 1: Using requirements.txt (Recommended for Streamlit Cloud)

Generate a requirements.txt from your uv environment:

```bash
uv pip freeze > requirements.txt
```

Then deploy normally to Streamlit Cloud.

### Option 2: Using pyproject.toml Directly

Streamlit Cloud now supports pyproject.toml! Just:
1. Push your code with pyproject.toml
2. Deploy to Streamlit Cloud
3. It will automatically install dependencies

**Important**: Set the main file path to `streamlit_app/app.py` in your Streamlit Cloud settings.

## Troubleshooting

### uv command not found
- Make sure uv is installed: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Restart your terminal after installation

### Import errors
- Ensure you're in the virtual environment: `source .venv/bin/activate`
- Reinstall in editable mode: `uv pip install -e .`

### Database is locked
- This happens with concurrent writes
- The framework is designed for single-writer scenarios
- Ensure you're not writing from multiple sessions simultaneously

### Session state not persisting
- Streamlit Cloud may reset sessions
- Critical data should be stored in the database, not just session state

## Why uv?

**uv** is a modern Python package installer that is:
- ⚡ **10-100x faster** than pip
- 🔒 **More reliable** with consistent dependency resolution
- 🎯 **Drop-in replacement** for pip (same commands work)
- 🚀 **Built in Rust** for maximum performance

Learn more: https://github.com/astral-sh/uv

## Migrating from pip/venv

If you have an existing setup with requirements.txt:

```bash
# Remove old virtual environment
rm -rf venv/

# Create new uv environment
uv venv

# Activate it
source .venv/bin/activate

# Install from pyproject.toml
uv pip install -e .
```

## Related Concepts to Learn

- **Streamlit Session State**: Understanding how Streamlit manages state across reruns
- **SQLite Transactions**: For data integrity when writing to the database
- **Password Hashing with bcrypt**: Security best practices for storing passwords
- **Streamlit Secrets Management**: For handling sensitive config in deployment
- **uv Package Management**: Modern Python dependency management

## References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [SQLite Python Tutorial](https://docs.python.org/3/library/sqlite3.html)
- [Streamlit Cloud Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Session State Documentation](https://docs.streamlit.io/library/api-reference/session-state)

## License

MIT License - feel free to use this template for your projects!

## Contributing

This is a template repository. Feel free to fork and customize for your needs!
