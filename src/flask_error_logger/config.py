import os
from datetime import datetime
from pathlib import Path
import secrets

SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))

current_path = Path(os.getcwd())
ERROR_DB = os.environ.get("ERROR_DB", current_path / ".." / "error_db.sqlite3")

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@admin.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "password")