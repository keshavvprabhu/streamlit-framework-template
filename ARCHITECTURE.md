# Framework Architecture

This document explains the architecture and design decisions of the Streamlit Framework Template.

## Overview

The framework follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│           Streamlit UI Layer            │
│  (app.py, pages/*.py, components/*.py)  │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│          Business Logic Layer           │
│         (core/auth.py, etc.)            │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│           Data Access Layer             │
│          (core/database.py)             │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│            SQLite Database              │
│              (data/app.db)              │
└─────────────────────────────────────────┘
```

## Directory Structure

### `/core` - Core Business Logic
Contains the essential functionality that powers the framework:

- **`auth.py`**: Authentication and user management
  - Password hashing with bcrypt
  - User CRUD operations
  - Role-based access control
  - Session validation

- **`database.py`**: Database connectivity
  - SQLite connection management
  - Database initialization
  - Table creation and schema management

- **`session.py`**: Session state management
  - Streamlit session state initialization
  - User session lifecycle
  - Session timeout handling

### `/components` - Reusable UI Components
Modular, reusable UI elements:

- **`footer.py`**: Footer component
  - Configurable copyright and version info
  - Dynamic link generation
  - Customizable styling

- **`user_management.py`**: User management UI
  - User creation forms
  - User listing and deletion
  - Password change interface

### `/config` - Configuration
Application-wide configuration:

- **`app_config.py`**: Centralized configuration
  - App metadata (name, version)
  - Footer settings
  - Database path
  - Session settings

### `/pages` - Multi-page Application
Streamlit's multi-page app structure:

- Files named `N_emoji_Page_Name.py`
- Number prefix controls order
- Each page can have its own authentication requirements

### `/scripts` - Utility Scripts
Administrative and setup scripts:

- **`init_db.py`**: Database initialization
  - Creates database schema
  - Sets up initial admin user
  - Can be run standalone

### `/data` - Data Storage
Database files (gitignored):

- **`app.db`**: Main SQLite database
- Excluded from version control
- Auto-created on first run

### `/.streamlit` - Streamlit Configuration
Streamlit-specific settings:

- **`config.toml`**: Theme and server settings
- Controls appearance and behavior

## Core Design Patterns

### 1. Separation of Concerns

Each module has a single, well-defined responsibility:

```python
# Database operations
from core.database import get_db_connection

# Authentication logic
from core.auth import authenticate_user

# UI components
from components import render_footer
```

### 2. Dependency Injection

Functions receive dependencies as parameters rather than importing them:

```python
def create_user(username: str, password: str, role: str = 'user'):
    # Uses get_db_connection() internally
    # But could be modified to accept a connection parameter
    pass
```

### 3. Decorator Pattern (Future Enhancement)

Current implementation uses explicit checks:
```python
if not require_auth():
    st.stop()
```

Could be enhanced with decorators:
```python
@require_auth
def my_page():
    # Page content
    pass
```

### 4. Factory Pattern

Database connections are created through a factory function:

```python
def get_db_connection() -> sqlite3.Connection:
    # Handles connection creation with consistent settings
    # Returns configured connection
    pass
```

## Authentication Flow

```
┌─────────────┐
│ User visits │
│    app      │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Session state   │
│ initialized?    │◄──── init_session_state()
└────────┬────────┘
         │
    ┌────▼────┐
    │Logged   │
    │in?      │
    └─┬───┬───┘
      │   │
   No │   │ Yes
      │   │
      ▼   ▼
   ┌──────────┐  ┌────────────┐
   │Show login│  │Show content│
   │form      │  │& logout    │
   └─────┬────┘  └────────────┘
         │
         ▼
   ┌──────────────┐
   │Authenticate  │
   │with username │
   │& password    │
   └──────┬───────┘
          │
     ┌────▼─────┐
     │Valid?    │
     └─┬────┬───┘
       │    │
    Yes│    │No
       │    │
       ▼    ▼
   ┌──────────┐  ┌────────────┐
   │Set       │  │Show error  │
   │session   │  │message     │
   │& rerun   │  └────────────┘
   └──────────┘
```

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Indexes:**
- `idx_username`: Fast username lookups

**Roles:**
- `admin`: Full access, can manage users
- `user`: Standard access

### Custom Tables

Add your own tables in `scripts/init_db.py`:

```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS your_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")
```

## Security Considerations

### Password Security

1. **Hashing**: bcrypt with salt
   ```python
   password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
   ```

2. **Never stored in plain text**

3. **Minimum password length**: 8 characters (configurable)

### SQL Injection Prevention

Uses parameterized queries:
```python
cursor.execute(
    "SELECT * FROM users WHERE username = ?",
    (username,)
)
```

Never use string formatting for SQL:
```python
# ❌ NEVER DO THIS
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
```

### Session Security

1. **Session state**: Stored server-side by Streamlit
2. **Timeout**: Configurable session timeout
3. **CSRF protection**: Enabled in Streamlit config

### Deployment Security

1. **HTTPS**: Automatic on Streamlit Cloud
2. **Secrets management**: Use Streamlit secrets for sensitive data
3. **Database location**: Never commit database to git

## Performance Considerations

### Database

1. **Connection pooling**: Not implemented (SQLite is lightweight)
2. **Indexes**: Created on frequently queried columns
3. **Connection closure**: Always close connections after use

### Caching

Streamlit provides built-in caching:

```python
@st.cache_data
def load_data():
    # Expensive operation
    return data
```

Use for:
- Database queries that rarely change
- Expensive computations
- External API calls

### Session State

Minimize session state usage:
- Store only necessary data
- Use database for persistence
- Clear unused state variables

## Scalability Limitations

### SQLite Constraints

1. **Concurrent writes**: Limited to one writer at a time
2. **File-based**: Not suitable for distributed systems
3. **Size limits**: Practical limit ~1TB (theoretical 140TB)

### Solutions for Scale

1. **PostgreSQL**: For production multi-user apps
2. **MongoDB**: For document-based data
3. **Redis**: For session management
4. **Separate API**: Move backend to FastAPI/Flask

## Extension Points

### Adding New Features

1. **New page**: Create file in `pages/`
2. **New component**: Add to `components/`
3. **New auth method**: Extend `core/auth.py`
4. **New database table**: Update `scripts/init_db.py`

### Custom Authentication

Replace the authentication system:

```python
# Instead of built-in auth
from your_auth import authenticate

if not authenticate():
    st.stop()
```

### External Database

Modify `core/database.py`:

```python
import psycopg2  # PostgreSQL

def get_db_connection():
    return psycopg2.connect(
        host="...",
        database="...",
        user="...",
        password="..."
    )
```

## Testing Strategy

### Unit Tests (Not Included)

Test individual functions:

```python
def test_hash_password():
    password = "test123"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
```

### Integration Tests

Test database operations:

```python
def test_create_user():
    init_database()
    assert create_user("test", "password123", "user")
    # Clean up
```

### UI Tests

Use Streamlit's testing framework:

```python
from streamlit.testing.v1 import AppTest

def test_login():
    app = AppTest.from_file("app.py")
    app.run()
    # Assert UI elements exist
```

## Best Practices

### Code Organization

1. **One responsibility per file**
2. **Clear imports at the top**
3. **Docstrings for all functions**
4. **Type hints where helpful**

### Error Handling

```python
try:
    # Operation
    pass
except Exception as e:
    st.error(f"Error: {e}")
    # Log error for debugging
```

### Documentation

1. **README**: User-facing documentation
2. **Docstrings**: Developer documentation
3. **Comments**: Explain complex logic
4. **ARCHITECTURE.md**: This file!

## Future Enhancements

### Planned Features

1. **Email verification**: For new users
2. **Password reset**: Via email
3. **Two-factor authentication**: Enhanced security
4. **Audit logging**: Track user actions
5. **API endpoints**: REST API for external access

### Migration Path

To add features:

1. Update database schema in `init_db.py`
2. Add business logic to `core/`
3. Create UI components in `components/`
4. Update pages as needed
5. Update documentation

## Troubleshooting Guide

### Common Issues

1. **Import errors**: Check `sys.path` and package structure
2. **Database locked**: Close all connections properly
3. **Session lost**: Check timeout settings
4. **Styling issues**: Clear browser cache

### Debug Mode

Enable Streamlit debug features:

```python
# In app.py
import streamlit as st

st.set_page_config(
    page_title="App",
    # Enable wide mode for debugging
    layout="wide"
)

# Show session state
with st.expander("Debug: Session State"):
    st.write(st.session_state)
```

## Contributing

To modify this framework:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Update documentation
6. Submit pull request

## License

MIT License - See LICENSE file for details.
