# ShareSecurely — Architecture Document

An open-source secure file-sharing platform designed for sharing sensitive documents with controlled access, expiration policies, and audit tracking.

---

## 1. Project Overview

**ShareSecurely** is a lightweight alternative to insecure file-sharing methods, providing a secure, auditable, and controlled environment for file transfer. It is built as a cybersecurity portfolio project demonstrating authentication, authorization, cryptography, secure file handling, and web application security.

### Key Capabilities

- Secure file uploads
- Controlled file access
- Expiring download links
- Password-protected sharing
- Download tracking
- Access auditing

---

## 2. Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.14, Flask 3.1, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Flask-Bcrypt, Flask-Migrate |
| **Frontend** | HTMX, Jinja2 Templates, Tailwind CSS |
| **Database** | MySQL (via PyMySQL), SQLite (alternative dev), PostgreSQL (alternative prod) |
| **Storage** | Local filesystem, S3-compatible storage (MinIO, Wasabi) |
| **Migrations** | Alembic / Flask-Migrate |
| **Security** | bcrypt (password hashing), SHA-256 (file integrity), CSRF protection, rate limiting |

### Python Dependencies

```
Flask==3.1.3
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.3.0
Flask-Bcrypt==1.0.1
Flask-Migrate==4.1.0
PyMySQL==1.2.0
bcrypt==5.0.0
python-dotenv==1.2.2
email-validator==2.3.0
alembic==1.18.5
```

---

## 3. Project Structure

```
sharesecurely/
├── run.py                     # Application entry point
├── requirements.txt           # Python dependencies
├── ARCHITECTURE.md            # This document
├── .env                       # Environment variables (ignored by git)
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore rules
├── app/
│   ├── __init__.py            # App factory (create_app)
│   ├── config.py              # Configuration class (env-based)
│   ├── extensions.py          # Flask extensions (SQLAlchemy)
│   ├── routes.py              # Main blueprint & home route
│   ├── auth/                  # Authentication module
│   ├── audit/                 # Audit logging module
│   ├── dashboard/             # User dashboard module
│   ├── files/                 # File management module
│   ├── models/                # Database models
│   ├── sharing/               # Secure sharing module
│   ├── static/                # Static assets (CSS, JS)
│   ├── templates/             # Jinja2 templates
│   │   ├── css/               # Template-specific CSS
│   │   └── js/                # Template-specific JS
│   └── utils/                 # Utility functions
├── instance/                  # Flask instance folder (ignored by git)
├── migrations/                # Alembic database migrations
├── uploads/                   # Uploaded files storage (ignored by git)
└── venv/                      # Python virtual environment (ignored by git)
```

---

## 4. Application Architecture

### Request Flow

```
Browser (HTMX Requests)
        │
        ▼
┌──────────────────┐
│  Flask Application│
│  (App Factory)    │
└──────┬───────────┘
       │
       ├──────────────► Database (MySQL/SQLite/PostgreSQL)
       ├──────────────► File Storage (Local / S3 / MinIO / Wasabi)
       └──────────────► Audit Logs
```

### App Factory Pattern

The application uses Flask's **app factory** pattern (`create_app()` in `app/__init__.py`):

1. `run.py` calls `create_app()`
2. Configuration is loaded from `Config` class (environment variables via `.env`)
3. Extensions (SQLAlchemy) are initialized
4. Blueprints are registered (currently `main` blueprint from `routes.py`)

### Configuration

All configuration is environment-driven via `python-dotenv`:

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Flask session signing key |
| `DB_USER` | Database username |
| `DB_PASSWORD` | Database password |
| `DB_HOST` | Database host |
| `DB_PORT` | Database port |
| `DB_NAME` | Database name |

---

## 5. Core Features

### 5.1 User Management

- **Features:** Registration, login/logout, profile management, account security settings
- **Security:** bcrypt password hashing, session protection, CSRF protection, rate limiting

### 5.2 File Management

- **User Actions:** Upload, view owned files, delete, rename, manage sharing permissions
- **File Storage:** Files stored outside the public directory; file type validation and size restrictions enforced

#### File Table Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (PK) | Unique identifier |
| `owner_id` | Integer (FK) | Reference to the user who uploaded the file |
| `filename` | String | Original or sanitized name of the file |
| `storage_path` | String | Path where the file is securely stored |
| `file_size` | Integer | Size of the file in bytes |
| `file_hash` | String | SHA-256 hash for integrity checking |
| `uploaded_at` | DateTime | Timestamp of upload |

### 5.3 Secure Sharing

- **Functionality:** Users create token-based sharing links (e.g., `https://sharesecurely.com/share/a82f91bc`)
- **Options:** Expiration dates, maximum download limits, password protection, manual link revocation

#### ShareLink Table Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (PK) | Unique identifier |
| `file_id` | Integer (FK) | Reference to the shared file |
| `token` | String | Secure random token for the URL |
| `password_hash` | String | Hashed password (if protected) |
| `expires_at` | DateTime | Date/time the link becomes invalid |
| `download_limit` | Integer | Maximum allowed downloads |
| `download_count` | Integer | Current number of times downloaded |
| `created_at` | DateTime | Timestamp of link creation |

### 5.4 Audit Logging

- **Tracked Events:** File uploads, share link creation, shared file access, failed download attempts, expired link access attempts

#### AuditLog Table Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (PK) | Unique identifier |
| `user_id` | Integer (FK) | User associated with the action (if applicable) |
| `action` | String | Description of the event |
| `ip_address` | String | Origin IP of the request |
| `timestamp` | DateTime | Time of the event |
| `metadata` | JSON/Text | Additional context/data |

---

## 6. Security Design

### File Security
- File type validation (allowlist approach)
- File size restrictions
- Secure filename sanitization
- Storage strictly outside the public web directory
- Future: malware scanning support

### Cryptography
- **Data Integrity:** SHA-256 file hashing to detect tampering
- **Access Control:** Secure random tokens (Python `secrets` module) for share links
- **Authentication:** Password hashing via Werkzeug/bcrypt

### Web Security
- CSRF protection (Flask-WTF)
- Session security (Flask-Login)
- Rate limiting on authentication endpoints
- Input validation and sanitization

---

## 7. Development Roadmap

### Phase 1: MVP *(2–3 weeks)*
- [ ] User authentication (register, login, logout)
- [ ] User dashboard
- [ ] File uploads & downloads
- [ ] Basic permissions

### Phase 2: Security Features *(2–3 weeks)*
- [ ] Expiring share links
- [ ] Password-protected shares
- [ ] Audit logging
- [ ] File hashing (SHA-256)
- [ ] Rate limiting

### Phase 3: Advanced Features *(3–4 weeks)*
- [ ] Malware scanning
- [ ] Email notifications
- [ ] File encryption at rest
- [ ] API access
- [ ] Admin dashboard

---

## 8. Testing Plan

| Type | Tools | Focus Areas |
|------|-------|-------------|
| **Unit Tests** | pytest | Authentication, permissions, file validation, token generation |
| **Security Scanning** | OWASP ZAP | XSS, CSRF, SQL injection, broken access control |
| **SAST** | Bandit, Semgrep | Python security vulnerabilities in source code |

---

## 9. Open Source Roadmap

### Version 1.0 Release
- Comprehensive documentation
- Installation guide
- Docker support
- Contribution guide

### Future Additions
- Organization accounts & team sharing
- Enterprise policies
- SSO integration (OAuth/OIDC)

---

## 10. Running the Application

### Prerequisites
- Python 3.10+
- MySQL database (or SQLite for development)
- Virtual environment (recommended)

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd sharesecurely

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials and secret key

# Run database migrations
flask db upgrade

# Start the application
python run.py
```

---

## 11. Portfolio Summary

> *"Developed an open-source secure file-sharing platform using Flask and HTMX with controlled access, cryptographic integrity verification, and audit logging."*
