import sqlite3
from pathlib import Path
from .config import DB_PATH, SCHEMA_PATH

def connect(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Connect to SQLite with sensible defaults."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")  # better concurrency
    return conn

def apply_schema(db_path: str = DB_PATH, schema_path: str = SCHEMA_PATH) -> None:
    """Apply SQL schema from file."""
    schema = Path(schema_path).read_text(encoding="utf-8")
    with connect(db_path) as conn:
        conn.executescript(schema)
    print(f"Schema applied successfully to {db_path}")

def seed_demo(db_path: str = DB_PATH) -> None:
    """Insert some sample data for quick testing."""
    with connect(db_path) as conn:
        cur = conn.cursor()

        # Airports
        cur.executemany(
            "INSERT OR IGNORE INTO airport(code, name, city, country) VALUES (?, ?, ?, ?)",
            [
                ("LHR", "Heathrow", "London", "UK"),
                ("DXB", "Dubai Intl", "Dubai", "UAE"),
                ("ISB", "Islamabad Intl", "Islamabad", "Pakistan"),
            ],
        )

        # Aircraft
        cur.executemany(
            "INSERT OR IGNORE INTO aircraft(model, capacity) VALUES (?, ?)",
            [
                ("Airbus A320", 180),
                ("Boeing 777-300ER", 396),
            ],
        )

        # Passengers
        cur.executemany(
            "INSERT OR IGNORE INTO passenger(name, email) VALUES (?, ?)",
            [
                ("Adnan Khan", "adnan@example.com"),
                ("Sara Malik", "sara@example.com"),
            ],
        )

        # Example flight
        cur.execute("""
            INSERT OR IGNORE INTO flight
              (code, departure_airport_id, arrival_airport_id,
               departure_time, arrival_time, aircraft_id, base_price)
            VALUES (
              'SL101',
              (SELECT id FROM airport WHERE code='LHR'),
              (SELECT id FROM airport WHERE code='DXB'),
              '2025-11-01T08:30:00',
              '2025-11-01T18:00:00',
              (SELECT id FROM aircraft WHERE model='Airbus A320'),
              199.50
            )
        """)

        conn.commit()
    print("Demo data seeded.")
