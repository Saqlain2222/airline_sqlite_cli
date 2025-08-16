import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SQLite database file path
DB_PATH = os.environ.get("DB_PATH", str(BASE_DIR / "airline.db"))

# SQL schema file path
SCHEMA_PATH = os.environ.get("SCHEMA_PATH", str(BASE_DIR / "models.sql"))
