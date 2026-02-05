# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-02-03

### Added
- Initial release of Streamlit Framework Template
- User authentication system with bcrypt password hashing
- SQLite database integration
- User management interface (admin only)
- Configurable footer component
- Session management with timeout
- Multi-page application structure
- Example XML generator page
- Comprehensive documentation (README, QUICKSTART, DEPLOYMENT, ARCHITECTURE)
- Database initialization script
- Streamlit Cloud deployment support

### Security
- Password hashing with bcrypt
- SQL injection prevention with parameterized queries
- Session timeout functionality
- CSRF protection enabled
- Role-based access control (admin/user)

## [Unreleased]

### Planned
- Email verification for new users
- Password reset functionality
- Two-factor authentication
- Audit logging
- REST API endpoints
- PostgreSQL support for production deployments

---

## How to Update This Changelog

When making changes, add them under `[Unreleased]` in the appropriate category:

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

When releasing a new version:
1. Move items from `[Unreleased]` to a new version section
2. Add the version number and date
3. Keep `[Unreleased]` section for future changes
