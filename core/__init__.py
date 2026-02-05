"""
Core modules for authentication, database, and session management.
"""

from .auth import (
    authenticate_user,
    create_user,
    require_auth,
    require_admin,
    logout,
    is_admin,
    get_all_users,
    update_user_password,
    delete_user,
)

from .database import (
    get_db_connection,
    init_database,
)

from .session import (
    init_session_state,
    set_authenticated_user,
    clear_session,
    get_current_user,
)

__all__ = [
    'authenticate_user',
    'create_user',
    'require_auth',
    'require_admin',
    'logout',
    'is_admin',
    'get_all_users',
    'update_user_password',
    'delete_user',
    'get_db_connection',
    'init_database',
    'init_session_state',
    'set_authenticated_user',
    'clear_session',
    'get_current_user',
]
