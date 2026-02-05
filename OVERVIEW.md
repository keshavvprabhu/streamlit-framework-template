# Streamlit Framework Template - uv Edition

## 🎯 What You've Got

A **production-ready Streamlit application framework** powered by **uv** for blazing-fast setup and dependency management!

### ✅ Core Features
- 🔐 **Authentication**: bcrypt password hashing, session management, login/logout
- 👥 **User Management**: Create/delete users, change passwords, role-based access (admin/user)  
- 💾 **SQLite Database**: Auto-initialization, easy connection management
- 🎨 **Configurable Footer**: Copyright, version, custom links
- 📄 **Multi-page Structure**: Automatic routing, emoji support
- 📋 **Example XML Generator**: Demonstrates form building, file downloads, database saves
- ⚡ **uv-powered**: 10-100x faster than pip for dependency management!

## ⚡ Quick Start (3 Minutes!)

```bash
# 1. Install uv (if needed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Create virtual environment
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies (⚡ super fast!)
uv pip install -e .

# 4. Initialize database
init-db

# 5. Run the app
streamlit run streamlit_app/app.py
```

**Default login**: `admin` / `changeme123`

## 📦 Project Structure

```
streamlit-framework-template/
├── pyproject.toml              # uv/pip configuration (replaces requirements.txt!)
├── .python-version             # Python version (3.11)
├── README.md                   # Full documentation
├── QUICKSTART.md              # 5-minute setup guide
├── LICENSE                     # MIT License
│
├── streamlit_app/              # Main Python package
│   ├── __init__.py
│   ├── app.py                 # Application entry point
│   ├── cli.py                 # CLI commands
│   │
│   ├── core/                  # Business logic
│   │   ├── auth.py           # Authentication & user mgmt
│   │   ├── database.py       # Database operations
│   │   └── session.py        # Session management
│   │
│   ├── components/            # Reusable UI components
│   │   ├── footer.py         # Footer component
│   │   └── user_management.py # User mgmt UI
│   │
│   ├── config/                # Configuration
│   │   └── app_config.py     # App settings
│   │
│   ├── pages/                 # Multi-page app pages
│   │   ├── 1_👤_User_Management.py
│   │   └── 2_📄_XML_Generator.py
│   │
│   ├── scripts/               # Utility scripts
│   │   └── init_db.py        # Database initialization
│   │
│   └── .streamlit/            # Streamlit config
│       └── config.toml       # Theme & settings
│
└── data/                      # Database storage
    └── app.db                # (created on first run)
```

## 🆚 Why uv Instead of pip?

### Traditional Setup (pip)
```bash
python -m venv venv           # ~5 seconds
source venv/bin/activate
pip install -r requirements.txt  # ~30 seconds
```
**Total: ~35 seconds** 🐌

### Modern Setup (uv)
```bash
uv venv                       # ~0.5 seconds
source .venv/bin/activate
uv pip install -e .          # ~2 seconds
```
**Total: ~3 seconds** ⚡

### Why It Matters

- ⚡ **10-100x faster** installations
- 🔒 **Better dependency resolution** (no conflicts)
- 🎯 **Drop-in replacement** for pip (same commands)
- 📦 **Uses pyproject.toml** (modern Python standard)
- 🦀 **Built in Rust** for maximum performance

## 🎁 What's Different from Standard pip Setup?

### 1. **pyproject.toml instead of requirements.txt**
Modern Python packaging standard, includes metadata, dependencies, and build config.

### 2. **Package Structure**
Code is organized as an installable Python package (`streamlit_app/`) instead of loose scripts.

### 3. **Entry Points**
Installed commands like `init-db` available system-wide.

### 4. **Editable Install**
`uv pip install -e .` means you can edit code and changes take effect immediately.

### 5. **Import Paths**
Use `from streamlit_app.core import ...` instead of relative imports.

## 📚 Key Files Explained

### `pyproject.toml`
The heart of the project. Defines:
- Package name and version
- Dependencies (streamlit, bcrypt)
- Entry points (scripts you can run)
- Development tools (pytest, black, ruff)

### `.python-version`
Tells uv which Python version to use. Change if needed:
```
3.11  # or 3.9, 3.10, 3.12, etc.
```

### `streamlit_app/app.py`
Main application file. Run with:
```bash
streamlit run streamlit_app/app.py
```

### `streamlit_app/scripts/init_db.py`
Database initialization. Can be run as:
```bash
init-db  # if installed
# or
uv run python -m streamlit_app.scripts.init_db
```

## 🚀 Common Commands

### Setup & Installation
```bash
# Create virtual environment
uv venv

# Activate (do this once per terminal session)
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install package + dependencies
uv pip install -e .

# Install with dev tools (pytest, black, ruff)
uv pip install -e ".[dev]"
```

### Running the App
```bash
# With activated venv
streamlit run streamlit_app/app.py

# Without activating (uv handles it)
uv run streamlit run streamlit_app/app.py
```

### Database Management
```bash
# Initialize database
init-db

# Or without venv activation
uv run init-db
```

### Adding Dependencies
```bash
# 1. Edit pyproject.toml, add to dependencies list:
dependencies = [
    "streamlit>=1.31.0",
    "bcrypt>=4.1.2",
    "pandas>=2.0.0",  # <- new dependency
]

# 2. Install
uv pip install -e .
```

### Development
```bash
# Run tests (if you add them)
uv run pytest

# Format code
uv run black streamlit_app/

# Lint code
uv run ruff check streamlit_app/

# Update all dependencies
uv pip install --upgrade -e .
```

## 🎨 Customization

### Change App Settings
Edit `streamlit_app/config/app_config.py`:
```python
APP_CONFIG = {
    "app_name": "My App",
    "version": "1.0.0",
    "copyright_holder": "My Company",
    # ... more settings
}
```

### Add a New Page
Create `streamlit_app/pages/3_🎯_My_Page.py`:
```python
import streamlit as st
from streamlit_app.core import require_auth
from streamlit_app.components import render_footer

st.set_page_config(page_title="My Page", page_icon="🎯")

if not require_auth():
    st.stop()

st.title("🎯 My Custom Page")
# Your code here

render_footer()
```

### Add Database Tables
Edit `streamlit_app/scripts/init_db.py`, find the `init_database()` function:
```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS my_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
```

## 🌐 Deployment to Streamlit Cloud

### Option 1: Generate requirements.txt
```bash
uv pip freeze > requirements.txt
```
Then deploy normally. Set main file: `streamlit_app/app.py`

### Option 2: Use pyproject.toml (Recommended)
Streamlit Cloud supports pyproject.toml! Just:
1. Push code to GitHub
2. Deploy on Streamlit Cloud
3. Set main file: `streamlit_app/app.py`

## 🔧 Migrating from pip Setup

If you have an old pip-based setup:

```bash
# Remove old environment
rm -rf venv/

# Create new uv environment
uv venv
source .venv/bin/activate

# Install from pyproject.toml
uv pip install -e .
```

Your old `requirements.txt` is no longer needed! Everything is in `pyproject.toml`.

## 📖 Related Concepts to Learn

1. **uv Package Manager** - Modern Python dependency management
2. **pyproject.toml** - Python's standard for project configuration
3. **Streamlit Session State** - How state works across reruns
4. **bcrypt Hashing** - Password security fundamentals
5. **SQLite ACID Properties** - Database transaction safety

## 🎓 Learning Resources

- [uv Documentation](https://github.com/astral-sh/uv)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Python Packaging Guide](https://packaging.python.org/en/latest/)
- [pyproject.toml Specification](https://peps.python.org/pep-0621/)

## 🐛 Troubleshooting

### uv not found
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart terminal
```

### Import errors
```bash
# Make sure you installed in editable mode
uv pip install -e .
```

### Database locked
- SQLite supports one writer at a time
- Close connections: `conn.close()`
- Don't write concurrently

### Streamlit not found
```bash
# Ensure dependencies installed
uv pip install -e .
# Check streamlit is in pyproject.toml dependencies
```

## 📝 Documentation Files

- **README.md** - Complete reference guide
- **QUICKSTART.md** - 5-minute setup walkthrough
- **LICENSE** - MIT License

## 🎉 You're Ready!

Your framework is configured for:
- ✅ Fast development with uv
- ✅ Modern Python packaging
- ✅ Production deployment
- ✅ Easy customization
- ✅ Secure authentication

Start building your XML generator or any other Streamlit app!

**Questions?** Check the README.md or QUICKSTART.md

---

**Built with ❤️ and ⚡ by uv**
