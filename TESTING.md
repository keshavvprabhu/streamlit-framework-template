# Testing Guide

This guide covers how to test your Streamlit Framework Template.

## Manual Testing Checklist

### Initial Setup Testing

- [ ] Clone repository successfully
- [ ] Create virtual environment
- [ ] Install dependencies without errors
- [ ] Run `python scripts/init_db.py` successfully
- [ ] Database file created at `data/app.db`
- [ ] Admin user created with default credentials

### Authentication Testing

#### Login Flow
- [ ] Login page appears when not authenticated
- [ ] Can log in with correct credentials
- [ ] Error message for incorrect username
- [ ] Error message for incorrect password
- [ ] Session persists across page navigation
- [ ] Logout button works correctly
- [ ] After logout, redirected to login

#### Password Security
- [ ] Passwords are hashed in database (not plain text)
- [ ] Cannot login with wrong password
- [ ] Can change password successfully
- [ ] New password works immediately
- [ ] Old password no longer works after change

### User Management Testing (Admin Only)

#### Create User
- [ ] Admin can access User Management page
- [ ] Regular user cannot access User Management page
- [ ] Can create user with valid credentials
- [ ] Error on duplicate username
- [ ] Error on password < 8 characters
- [ ] Error on username < 3 characters
- [ ] Error on password mismatch
- [ ] Both 'admin' and 'user' roles work

#### View Users
- [ ] All users displayed correctly
- [ ] Username shown
- [ ] Role badge displayed (admin/user)
- [ ] User ID visible
- [ ] Current user marked as "You"

#### Delete User
- [ ] Can delete other users
- [ ] Cannot delete yourself
- [ ] User removed from database
- [ ] Cannot login with deleted user

### Footer Testing

- [ ] Footer appears on all pages
- [ ] Copyright year displays correctly
- [ ] Version number displays correctly
- [ ] All footer links work
- [ ] Links open in new tab
- [ ] Footer styling consistent

### XML Generator Testing

- [ ] Page loads for authenticated users
- [ ] Form fields accept input
- [ ] Generate button creates XML
- [ ] XML displays correctly
- [ ] Download button works
- [ ] Downloaded file contains correct XML
- [ ] Save to database works
- [ ] Saved messages appear in list

### Database Testing

- [ ] Database file created automatically
- [ ] Users table has correct schema
- [ ] Indexes created on username
- [ ] Foreign key constraints work
- [ ] Timestamps auto-populate
- [ ] Connection closes properly

### Session Testing

- [ ] Session persists during use
- [ ] Session timeout works (if configured)
- [ ] Session cleared on logout
- [ ] No session leaks between users

### Multi-Page Testing

- [ ] Main page accessible
- [ ] User Management page in sidebar
- [ ] XML Generator page in sidebar
- [ ] Page numbers control order
- [ ] Emojis display in sidebar
- [ ] Can navigate between pages

### UI/UX Testing

- [ ] Pages load quickly
- [ ] No broken layouts
- [ ] Forms are clear and usable
- [ ] Error messages are helpful
- [ ] Success messages appear
- [ ] No console errors in browser

### Security Testing

- [ ] SQL injection prevented (try: `' OR '1'='1`)
- [ ] Password fields hide input
- [ ] CSRF protection enabled
- [ ] No passwords in logs
- [ ] No sensitive data in URLs

## Automated Testing (Future)

### Unit Tests

Create `tests/test_auth.py`:

```python
import pytest
from core.auth import hash_password, verify_password, create_user
from core.database import init_database
import os

@pytest.fixture
def test_db():
    """Create a test database."""
    test_db_path = "test_app.db"
    os.environ['DB_PATH'] = test_db_path
    init_database()
    yield test_db_path
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

def test_password_hashing():
    """Test password hashing and verification."""
    password = "testpass123"
    hashed = hash_password(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrongpass", hashed)

def test_create_user(test_db):
    """Test user creation."""
    assert create_user("testuser", "password123", "user")
    assert not create_user("testuser", "password123", "user")  # Duplicate

def test_user_roles(test_db):
    """Test different user roles."""
    assert create_user("admin_user", "pass123", "admin")
    assert create_user("regular_user", "pass123", "user")
```

Run tests:
```bash
pytest tests/
```

### Integration Tests

Create `tests/test_integration.py`:

```python
import pytest
from core import authenticate_user, create_user, get_all_users
from core.database import init_database

def test_full_auth_flow():
    """Test complete authentication flow."""
    init_database()
    
    # Create user
    assert create_user("integrationtest", "password123", "user")
    
    # Authenticate
    user = authenticate_user("integrationtest", "password123")
    assert user is not None
    assert user['username'] == "integrationtest"
    assert user['role'] == "user"
    
    # Wrong password
    assert authenticate_user("integrationtest", "wrongpass") is None
```

### Streamlit UI Tests

Create `tests/test_app.py`:

```python
from streamlit.testing.v1 import AppTest

def test_app_runs():
    """Test that the app runs without errors."""
    app = AppTest.from_file("app.py")
    app.run()
    assert not app.exception

def test_login_form_exists():
    """Test that login form is present."""
    app = AppTest.from_file("app.py")
    app.run()
    
    # Check for login elements
    assert len(app.text_input) >= 2  # Username and password
```

## Performance Testing

### Load Testing

Test with multiple concurrent users:

```python
# locustfile.py
from locust import HttpUser, task, between

class StreamlitUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def view_homepage(self):
        self.client.get("/")
```

Run:
```bash
pip install locust
locust -f locustfile.py
```

### Database Performance

Test query performance:

```python
import time
from core.database import get_db_connection

def test_query_performance():
    """Test database query speed."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    start = time.time()
    cursor.execute("SELECT * FROM users")
    cursor.fetchall()
    duration = time.time() - start
    
    assert duration < 0.1  # Should be fast
    conn.close()
```

## Deployment Testing

### Streamlit Cloud

Before deploying:

- [ ] `requirements.txt` is up to date
- [ ] No hardcoded paths or credentials
- [ ] Database initialization works on first run
- [ ] All imports resolve correctly
- [ ] No local file dependencies

### Test on Streamlit Cloud

After deploying:

- [ ] App loads without errors
- [ ] Database initializes on first run
- [ ] Login works
- [ ] All pages accessible
- [ ] Footer displays correctly
- [ ] Downloads work
- [ ] No 502/503 errors

## Regression Testing

When making changes, retest:

1. **Authentication flow**
2. **User management**
3. **Database operations**
4. **Page navigation**
5. **Form submissions**

## Bug Report Template

When you find a bug:

```markdown
## Bug Description
[Clear description of the issue]

## Steps to Reproduce
1. Go to...
2. Click on...
3. Enter...
4. See error

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: [e.g., macOS 13]
- Python version: [e.g., 3.11]
- Streamlit version: [e.g., 1.31]
- Browser: [e.g., Chrome 120]

## Screenshots
[If applicable]

## Error Messages
```
[Error text or logs]
```
```

## Testing Best Practices

1. **Test early and often**: Don't wait until the end
2. **Test edge cases**: Empty inputs, very long inputs, special characters
3. **Test as different users**: Admin and regular users
4. **Test on different browsers**: Chrome, Firefox, Safari
5. **Test on different devices**: Desktop, tablet, mobile
6. **Document issues**: Keep track of bugs found and fixed

## Continuous Testing

Add to your development workflow:

```bash
# Before committing
1. Run manual tests on changed features
2. Check no console errors
3. Test login/logout
4. Test database operations
5. Review changed files
```

## Need Help?

If tests fail:
1. Check error messages carefully
2. Review logs in terminal
3. Check browser console
4. Verify database state
5. Ask on Streamlit forum

Happy testing! 🧪
