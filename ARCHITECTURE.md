# ShareSecurely Architecture

ShareSecurely is an open-source secure file-sharing platform for sharing sensitive documents with controlled access, expiration policies, password-protected links, download tracking, and audit trails.

This document is the long-term architecture reference for the project. It describes both the current application shell and the target architecture, so planned features are explicitly marked as planned rather than implied as already implemented.

---

## 1. Objectives

ShareSecurely is intended to be a lightweight alternative to sending confidential files through email attachments, open cloud links, or other hard-to-audit channels.

Primary goals:

- Provide secure file upload, storage, sharing, and download flows.
- Keep uploaded files outside the public web root.
- Control access with authentication, authorization, expiring links, password protection, and download limits.
- Record auditable security events such as uploads, share creation, successful downloads, failed access attempts, and expired-link attempts.
- Demonstrate practical cybersecurity engineering: authentication, authorization, cryptography, secure file handling, web security, and operational auditability.

Non-goals for the early MVP:

- Real-time collaboration.
- Public file browsing.
- Enterprise SSO or organization policy controls.
- End-to-end encryption between two browser clients.

---

## 2. Current Status

The repository currently contains:

- Flask application factory in `app/__init__.py`.
- Environment-based configuration in `app/config.py`.
- Shared Flask extensions in `app/extensions.py`:
  - SQLAlchemy
  - Flask-WTF CSRF protection
  - Flask-Migrate
- A public-page blueprint in `app/routes.py`.
- Jinja2 templates for the landing, contributors, contact, waitlist, terms, and privacy pages.
- Static assets under `app/static/`, with images under `app/static/images/`.
- Placeholder module directories for planned product features:
  - `auth`
  - `audit`
  - `dashboard`
  - `files`
  - `models`
  - `sharing`
  - `utils`

The current contact and waitlist forms are presentation placeholders. They accept CSRF-protected `POST` requests and redirect back to their own pages, but they do not persist submissions, send email, or create application records yet.

Planned but not implemented yet:

- User registration, login, logout, and profile management.
- File upload, download, delete, rename, and ownership management.
- Secure share-link creation and revocation.
- Password-protected share links.
- Download limits and expiration enforcement.
- Audit-log persistence.
- Rate limiting.
- File hashing and validation.

---

## 3. Technology Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.14 target, Flask 3.1 |
| Application extensions | Flask-SQLAlchemy, Flask-Login, Flask-WTF, Flask-Bcrypt, Flask-Migrate |
| Frontend | Jinja2 templates, HTMX, Alpine.js, Tailwind CSS |
| Database | MySQL via PyMySQL, SQLite for local development, PostgreSQL as a production alternative |
| Storage | Local filesystem first, S3-compatible storage later such as MinIO or Wasabi |
| Migrations | Alembic through Flask-Migrate |
| Security | CSRF protection, bcrypt password hashing, SHA-256 file integrity, rate limiting |
| Testing and scanning | pytest, OWASP ZAP, Bandit, Semgrep |

### Frontend Responsibilities

- Use Jinja2 for server-rendered pages, shared layout, and reusable template partials.
- Use HTMX when the server should return HTML fragments for progressive interactions.
- Use Alpine.js for small client-side UI state such as toggles, menus, disclosure controls, and temporary form behavior.
- Keep reusable CSS and JavaScript under `app/static/`.
- Keep images, logos, icons, and avatars under `app/static/images/`.
- Do not place CSS or JavaScript under `app/templates/` unless a future feature truly needs dynamically rendered script/style fragments.

### Python Dependencies

Core dependencies are pinned in `requirements.txt`. Important direct dependencies include:

```text
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

## 4. Project Structure

```text
sharesecurely/
|-- run.py                     # Application entry point
|-- requirements.txt           # Python dependencies
|-- README.md                  # Public project summary
|-- ARCHITECTURE.md            # Architecture and implementation reference
|-- .env                       # Local environment variables, ignored by git
|-- .env.example               # Environment variable template
|-- .gitignore                 # Git ignore rules
|-- app/
|   |-- __init__.py            # App factory, create_app()
|   |-- config.py              # Environment-based configuration
|   |-- extensions.py          # Shared extension instances
|   |-- routes.py              # Current public-page blueprint
|   |-- auth/                  # Planned authentication module
|   |-- audit/                 # Planned audit logging module
|   |-- dashboard/             # Planned authenticated dashboard module
|   |-- files/                 # Planned file management module
|   |-- models/                # Planned database models
|   |-- sharing/               # Planned secure sharing module
|   |-- static/
|   |   |-- css/               # Stylesheets
|   |   |-- js/                # Browser JavaScript
|   |   `-- images/            # Images, logos, icons, avatars
|   |-- templates/             # Jinja2 templates
|   `-- utils/                 # Planned shared utility functions
|-- instance/                  # Flask instance folder, ignored by git
|-- migrations/                # Alembic migration files
|-- uploads/                   # Local uploaded file storage, ignored by git
`-- venv/                      # Local virtual environment, ignored by git
```

---

## 5. Application Flow

```text
Browser
  |
  |-- normal page requests
  |-- HTMX partial requests
  |-- Alpine.js local UI behavior
  v
Flask application
  |
  |-- app factory: create_app()
  |-- configuration: Config
  |-- extensions: SQLAlchemy, CSRF, Flask-Migrate
  |-- blueprints: main now, feature modules later
  |
  |-- database: SQLite, MySQL, or PostgreSQL
  |-- file storage: local filesystem or S3-compatible backend
  `-- audit logs
```

### App Factory

`run.py` imports and calls `create_app()` from `app/__init__.py`.

The factory is responsible for:

- Creating the Flask application.
- Loading `Config`.
- Initializing extensions.
- Registering blueprints.

Future feature modules should expose blueprints and register them in the app factory. They should not create their own Flask app instances.

### Blueprint Boundaries

Current:

- `main`: public marketing and informational pages.

Planned:

- `auth`: registration, login, logout, password/security settings.
- `dashboard`: authenticated user landing area.
- `files`: upload, list, rename, delete, and download owned files.
- `sharing`: share-link creation, public share access, password checks, expiration checks, and revocation.
- `audit`: audit-log recording and viewing.

---

## 6. Configuration

Configuration is loaded from environment variables via `python-dotenv`.

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Flask session signing and CSRF key |
| `FLASK_ENV` | Environment name; production requires an explicit `SECRET_KEY` |
| `DATABASE_URL` | Optional complete SQLAlchemy database URI |
| `DB_USER` | MySQL database username |
| `DB_PASSWORD` | MySQL database password |
| `DB_HOST` | MySQL database host |
| `DB_PORT` | MySQL database port |
| `DB_NAME` | MySQL database name |

Database configuration precedence:

1. Use `DATABASE_URL` when present.
2. Otherwise build a MySQL URI from `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, and `DB_NAME`.
3. Otherwise fall back to SQLite at `instance/sharesecurely.db`.

Security rule:

- Production deployments must set a strong `SECRET_KEY`.
- Local development can fall back to a development-only key.

---

## 7. Domain Model

The exact SQLAlchemy model definitions are planned, but the core entities should follow these boundaries.

### User

Represents an authenticated account.

Expected fields:

| Field | Purpose |
|-------|---------|
| `id` | Unique identifier |
| `email` | Login identity, unique |
| `password_hash` | bcrypt password hash |
| `display_name` | Human-readable user name |
| `created_at` | Account creation timestamp |
| `updated_at` | Last profile/security update timestamp |

### File

Represents metadata for an uploaded file. The file bytes are stored outside the public web directory.

Expected fields:

| Field | Purpose |
|-------|---------|
| `id` | Unique identifier |
| `owner_id` | User who uploaded the file |
| `filename` | Original or sanitized display name |
| `storage_path` | Internal storage location |
| `file_size` | Size in bytes |
| `file_hash` | SHA-256 hash for integrity checking |
| `content_type` | Validated MIME/content type |
| `uploaded_at` | Upload timestamp |

### ShareLink

Represents a tokenized access path for a file.

Expected fields:

| Field | Purpose |
|-------|---------|
| `id` | Unique identifier |
| `file_id` | Shared file |
| `token` | Secure random URL token |
| `password_hash` | Optional bcrypt hash for protected links |
| `expires_at` | Date/time the link becomes invalid |
| `download_limit` | Maximum allowed downloads |
| `download_count` | Number of successful downloads |
| `revoked_at` | Timestamp for manual revocation |
| `created_at` | Creation timestamp |

### AuditLog

Represents security-relevant activity.

Expected fields:

| Field | Purpose |
|-------|---------|
| `id` | Unique identifier |
| `user_id` | Related user, when available |
| `action` | Event name, such as `file.uploaded` or `share.download_failed` |
| `ip_address` | Origin IP address |
| `user_agent` | Request user agent, when useful |
| `timestamp` | Event timestamp |
| `metadata` | JSON/Text details for the event |

---

## 8. Core Feature Design

### User Management

Status: planned.

Responsibilities:

- Register users.
- Authenticate users.
- Log users out.
- Manage profile and account security settings.
- Protect authenticated pages with Flask-Login.
- Hash passwords with bcrypt.
- Apply rate limiting to authentication endpoints.

### File Management

Status: planned.

Responsibilities:

- Validate file size and type before storage.
- Sanitize file names before persistence.
- Store files outside the public web root.
- Store metadata in the database.
- Compute and persist SHA-256 hashes.
- Let users view, rename, delete, and download their own files.
- Ensure users cannot access files they do not own.

### Secure Sharing

Status: planned.

Responsibilities:

- Create unguessable token-based share links.
- Enforce expiration dates.
- Enforce maximum download counts.
- Support optional password protection.
- Support manual revocation.
- Log successful and failed access attempts.

Example public share shape:

```text
https://sharesecurely.com/share/a82f91bc
```

### Audit Logging

Status: planned.

Responsibilities:

- Record file uploads.
- Record share-link creation and revocation.
- Record successful shared-file access.
- Record failed password attempts.
- Record expired, revoked, or over-limit link attempts.
- Preserve enough metadata to support security review without storing unnecessary sensitive data.

---

## 9. Security Design

### File Security

- Use an allowlist for accepted file types.
- Enforce maximum file sizes.
- Sanitize original filenames.
- Store file bytes outside `app/static/` and outside all public routes.
- Never serve uploaded files by direct static path.
- Use controlled Flask routes for downloads.
- Consider malware scanning as a later advanced feature.

### Cryptography

- Use bcrypt for user passwords and share-link passwords.
- Use Python's `secrets` module for share tokens.
- Use SHA-256 for file integrity hashes.
- Do not use SHA-256 as a password hashing mechanism.

### Web Security

- Keep CSRF protection enabled for state-changing forms.
- Use Flask-Login for session management once authentication is implemented.
- Add rate limiting before exposing authentication or public share-password endpoints.
- Validate and sanitize all user input.
- Avoid leaking whether a token exists when handling public share failures.
- Return generic errors for unauthorized share access while logging specific server-side reasons.

### Storage Security

- Local storage should use a non-public `uploads/` directory.
- S3-compatible storage should use private buckets by default.
- Download responses should be generated only after authorization and share-policy checks.
- Storage paths should be internal identifiers, not user-controlled paths.

---

## 10. Testing Strategy

### Unit Tests

Use pytest for:

- Authentication behavior.
- Permission checks.
- File validation.
- Token generation and expiration logic.
- Download-limit enforcement.
- Audit-log event creation.

### Integration Tests

Use Flask's test client for:

- Public routes.
- CSRF behavior.
- Login/logout flows.
- Upload/download flows.
- Share-link access flows.

### Security Testing

Use:

- OWASP ZAP for dynamic testing.
- Bandit for Python security linting.
- Semgrep for static analysis.

Focus areas:

- XSS.
- CSRF.
- SQL injection.
- Broken access control.
- Unsafe file handling.
- Token leakage.

---

## 11. Roadmap

### Phase 1: MVP, 2-3 weeks

- [ ] User registration, login, and logout.
- [ ] Authenticated dashboard.
- [ ] File upload and download.
- [ ] Basic ownership permissions.

### Phase 2: Security Features, 2-3 weeks

- [ ] Expiring share links.
- [ ] Password-protected share links.
- [ ] Manual share revocation.
- [ ] Audit logging.
- [ ] File hashing with SHA-256.
- [ ] Rate limiting.

### Phase 3: Advanced Features, 3-4 weeks

- [ ] Malware scanning.
- [ ] Email notifications.
- [ ] File encryption at rest.
- [ ] API access.
- [ ] Admin dashboard.

### Future Open-Source Milestones

- Comprehensive documentation.
- Installation guide.
- Docker support.
- Contribution guide.
- Organization accounts and team sharing.
- Enterprise policies.
- SSO integration with OAuth/OIDC.

---

## 12. Running the Application

### Prerequisites

- Python 3.10+ for local development.
- MySQL or SQLite.
- Virtual environment.

### Setup

```bash
git clone <repo-url>
cd sharesecurely

python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

pip install -r requirements.txt

cp .env.example .env
# Edit .env with a secret key and database settings.

flask db upgrade
python run.py
```

---

## 13. Portfolio Summary

> "Developed an open-source secure file-sharing platform using Flask, HTMX, and Alpine.js with controlled access, cryptographic integrity verification, and audit logging."
