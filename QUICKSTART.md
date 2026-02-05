# Quick Start Guide (uv)

Get your Streamlit app up and running in 5 minutes with **uv**!

## 🚀 Installation

### Step 0: Install uv (if not already installed)

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

Restart your terminal after installation.

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd streamlit-framework-template
```

### 2. Create Virtual Environment with uv
```bash
uv venv
```

This creates a `.venv` directory with a Python virtual environment.

### 3. Activate Virtual Environment

```bash
# On macOS/Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

Your prompt should now show `(.venv)` at the beginning.

### 4. Install Dependencies with uv
```bash
uv pip install -e .
```

This installs the package and all dependencies (streamlit, bcrypt) in seconds!

### 5. Initialize the Database
```bash
# Using the installed command
init-db

# Or run directly
uv run python -m streamlit_app.scripts.init_db
```

You should see:
```
✅ Database tables created successfully!
✅ Admin user created successfully!

📝 Default credentials:
   Username: admin
   Password: changeme123

⚠️  IMPORTANT: Change this password immediately after first login!
```

### 6. Run the App
```bash
# If venv is activated
streamlit run streamlit_app/app.py

# Or use uv run (no activation needed)
uv run streamlit run streamlit_app/app.py
```

The app will open in your browser at `http://localhost:8501`

## 🔐 First Login

1. Look at the sidebar on the left
2. Enter the default credentials:
   - **Username**: `admin`
   - **Password**: `changeme123`
3. Click "Login"

## 🔑 Change Your Password

**IMPORTANT: Do this immediately!**

1. After logging in, click on "User Management" in the sidebar
2. Go to the "Change Password" tab
3. Enter your current password (`changeme123`)
4. Enter a new strong password
5. Click "Change Password"

## 👥 Create Additional Users

1. Navigate to "User Management" (admin only)
2. Go to the "Create User" tab
3. Fill in:
   - Username (min 3 characters)
   - Password (min 8 characters)
   - Role (admin or user)
4. Click "Create User"

## 📄 Try the XML Generator

1. Click on "XML Generator" in the sidebar
2. Fill in the form:
   - Choose a message type
   - Enter receiver name
   - Write your message content
3. Click "Generate XML"
4. Download or save to database

## ⚡ Why uv?

**uv is 10-100x faster than pip!**

Traditional setup:
```bash
python -m venv venv           # ~5 seconds
source venv/bin/activate
pip install -r requirements.txt  # ~30 seconds
```

With uv:
```bash
uv venv                       # ~0.5 seconds
source .venv/bin/activate
uv pip install -e .          # ~2 seconds
```

**Result**: Setup goes from ~35 seconds to ~3 seconds! ⚡

## 🎨 Customize Your App

### Change the Footer

Edit `streamlit_app/config/app_config.py`:

```python
APP_CONFIG = {
    "app_name": "My Awesome App",  # Change this
    "version": "1.0.0",
    "copyright_year": "2024",
    "copyright_holder": "My Company",  # Change this
    "footer_links": [
        {"text": "Website", "url": "https://mycompany.com"},
        {"text": "Support", "url": "mailto:support@mycompany.com"},
    ],
}
```

### Change the Theme

Edit `streamlit_app/.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF4B4B"        # Main accent color
backgroundColor = "#FFFFFF"      # Page background
secondaryBackgroundColor = "#F0F2F6"  # Sidebar background
textColor = "#262730"           # Text color
```

### Add Your Own Page

1. Create a new file in `streamlit_app/pages/` directory
2. Name it: `3_🎯_My_Page.py` (number determines order)
3. Copy this template:

```python
import streamlit as st
from streamlit_app.core import require_auth
from streamlit_app.components import render_footer

st.set_page_config(page_title="My Page", page_icon="🎯")

if not require_auth():
    st.stop()

st.title("🎯 My Custom Page")
st.write("Your content here!")

render_footer()
```

## 💾 Add Custom Database Tables

Edit `streamlit_app/scripts/init_db.py` and add your tables in the `init_database()` function:

```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS my_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
```

Then re-run:
```bash
init-db
```

## 🔧 Common uv Commands

```bash
# Install package in editable mode
uv pip install -e .

# Install with dev dependencies
uv pip install -e ".[dev]"

# Add a new package
# Edit pyproject.toml, then:
uv pip install -e .

# Update all packages
uv pip install --upgrade -e .

# Run without activating venv
uv run streamlit run streamlit_app/app.py

# Run database init without activating venv
uv run init-db

# Generate requirements.txt (for deployment)
uv pip freeze > requirements.txt
```

## 🔍 Common Tasks

### Access the Database in Your Code

```python
from streamlit_app.core import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

# Query
cursor.execute("SELECT * FROM users")
results = cursor.fetchall()

# Insert
cursor.execute("INSERT INTO my_table (name) VALUES (?)", ("Test",))
conn.commit()

conn.close()
```

### Protect a Page with Authentication

```python
from streamlit_app.core import require_auth

if not require_auth():
    st.stop()

# Your protected content here
```

### Require Admin Access

```python
from streamlit_app.core import require_admin

if not require_admin():
    st.stop()

# Admin-only content here
```

### Get Current User Info

```python
from streamlit_app.core import get_current_user

user = get_current_user()
if user:
    st.write(f"Hello, {user['username']}!")
    st.write(f"Role: {user['role']}")
```

## 🐛 Troubleshooting

### "uv: command not found"
- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Restart your terminal
- Run `uv --version` to verify

### "ModuleNotFoundError: No module named 'streamlit_app'"
- Make sure you installed in editable mode: `uv pip install -e .`
- Ensure you're in the project root directory

### "Database is locked"
- Close all connections: `conn.close()`
- SQLite doesn't handle concurrent writes well
- Only write from one place at a time

### Login Not Working
- Check you initialized the database: `init-db`
- Verify the database file exists: `ls data/app.db`
- Check for typos in username/password

### Changes Not Appearing
- Streamlit caches some things
- Press `R` in the terminal to rerun
- Or press `C` to clear cache and rerun

## 📦 Development Workflow

1. **Make changes** to your code
2. **Streamlit auto-reloads** when you save files
3. **Add dependencies** by editing `pyproject.toml`
4. **Run `uv pip install -e .`** to install new dependencies
5. **Test** your changes
6. **Commit** to git

## 🚀 Deploy to Streamlit Cloud

### Option 1: Generate requirements.txt

```bash
uv pip freeze > requirements.txt
```

Then deploy normally. Set main file to: `streamlit_app/app.py`

### Option 2: Use pyproject.toml directly

Streamlit Cloud supports pyproject.toml! Just push and deploy.

**Important**: Set the main file path to `streamlit_app/app.py`

## 📚 Next Steps

1. Read the full [README.md](README.md)
2. Explore the example XML Generator page
3. Add your own features!
4. Check out [uv documentation](https://github.com/astral-sh/uv)

## 🆘 Need Help?

- Check the [Streamlit Documentation](https://docs.streamlit.io/)
- Learn more about [uv](https://github.com/astral-sh/uv)
- Ask on [Streamlit Forum](https://discuss.streamlit.io/)

Happy building with uv! ⚡🎉
