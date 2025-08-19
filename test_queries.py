import sqlite3
from datetime import datetime
import hashlib
import os

DB_FILE = "airline.db"


def hash_password(password: str, salt: bytes) -> bytes:
    """Hash password with salt using SHA-256 (demo only, not production-safe)."""
    return hashlib.sha256(salt + password.encode("utf-8")).digest()


def seed_data(conn):
    cur = conn.cursor()

    # Clear existing data (respect foreign key order)
    cur.executescript("""
    DELETE FROM crew_assignment;
    DELETE FROM crew_member;
    DELETE FROM ticket;
    DELETE FROM booking;
    DELETE FROM flight;
    DELETE FROM passenger;
    DELETE FROM aircraft;
    DELETE FROM airport;
    DELETE FROM user;
    """)

    # Airports (UK focus)
    cur.executemany("""
    INSERT INTO airport (code, name, city, country)
    VALUES (?, ?, ?, ?)
    """, [
        ("LHR", "Heathrow", "London", "UK"),
        ("MAN", "Manchester Airport", "Manchester", "UK"),
        ("EDI", "Edinburgh Airport", "Edinburgh", "UK"),
        ("JFK", "John F. Kennedy Intl", "New York", "USA"),
    ])

    # Aircraft
    cur.executemany("""
    INSERT INTO aircraft (model, capacity)
    VALUES (?, ?)
    """, [
        ("Airbus A320", 180),
        ("Boeing 777-300ER", 396),
        ("Embraer E190", 100),
    ])

    # Passengers
    cur.executemany("""
    INSERT INTO passenger (name, email)
    VALUES (?, ?)
    """, [
        ("Alice Johnson", "alice.johnson@example.com"),
        ("David Lee", "david.lee@example.com"),
        ("Sara Malik", "sara.malik@example.com"),
        ("John Smith", "john.smith@example.com"),
    ])

    # Flights
    cur.executemany("""
    INSERT INTO flight (code, departure_airport_id, arrival_airport_id,
                        departure_time, arrival_time, aircraft_id, base_price)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        ("BA210", 1, 3, "2025-09-27T10:00:00", "2025-09-27T11:20:00", 1, 120.0),
        ("EZ450", 2, 1, "2025-09-28T16:45:00", "2025-09-28T17:55:00", 3, 80.0),
        ("VS501", 1, 4, "2025-10-05T12:00:00", "2025-10-05T15:00:00", 2, 500.0),
    ])

    # Bookings
    cur.executemany("""
    INSERT INTO booking (passenger_id, flight_id, status, booked_at, price)
    VALUES (?, ?, ?, ?, ?)
    """, [
        (1, 1, "BOOKED", datetime.now().isoformat(), 125.0),
        (2, 1, "BOOKED", datetime.now().isoformat(), 120.0),
        (3, 2, "BOOKED", datetime.now().isoformat(), 90.0),
        (4, 3, "BOOKED", datetime.now().isoformat(), 520.0),
    ])

    # Tickets
    cur.executemany("""
    INSERT INTO ticket (booking_id, ticket_no, seat_no, class)
    VALUES (?, ?, ?, ?)
    """, [
        (1, "UKT001", "12A", "ECONOMY"),
        (2, "UKT002", "14C", "ECONOMY"),
        (3, "UKT003", "2B", "ECONOMY"),
        (4, "UKT004", "1A", "BUSINESS"),
    ])

    # Crew members
    cur.executemany("""
    INSERT INTO crew_member (name, role)
    VALUES (?, ?)
    """, [
        ("James Walker", "Pilot"),
        ("Emma Green", "Co-Pilot"),
        ("Sophie Taylor", "Cabin Crew"),
    ])

    # Crew assignments
    cur.executemany("""
    INSERT INTO crew_assignment (crew_member_id, flight_id, duty)
    VALUES (?, ?, ?)
    """, [
        (1, 1, "Captain"),
        (2, 1, "First Officer"),
        (3, 1, "Cabin Service"),
        (3, 2, "Cabin Service"),
    ])

    # Users (with password hashing demo)
    salt1 = os.urandom(16)
    salt2 = os.urandom(16)
    cur.executemany("""
    INSERT INTO user (username, password_hash, salt, role)
    VALUES (?, ?, ?, ?)
    """, [
        ("admin", hash_password("admin123", salt1), salt1, "ADMIN"),
        ("staff1", hash_password("staffpass", salt2), salt2, "STAFF"),
    ])

    conn.commit()


def run_queries(conn):
    cur = conn.cursor()

    print("\n=== Airports ===")
    for row in cur.execute("SELECT * FROM airport;"):
        print(row)

    print("\n=== Aircraft ===")
    for row in cur.execute("SELECT * FROM aircraft;"):
        print(row)

    print("\n=== Passengers ===")
    for row in cur.execute("SELECT * FROM passenger;"):
        print(row)

    print("\n=== Flights ===")
    for row in cur.execute("""
        SELECT f.code, a1.code, a2.code, f.departure_time, f.arrival_time
        FROM flight f
        JOIN airport a1 ON f.departure_airport_id=a1.id
        JOIN airport a2 ON f.arrival_airport_id=a2.id
    """):
        print(row)

    print("\n=== Bookings ===")
    for row in cur.execute("""
        SELECT b.id, p.name, f.code, b.price, b.status
        FROM booking b
        JOIN passenger p ON b.passenger_id=p.id
        JOIN flight f ON b.flight_id=f.id
    """):
        print(row)

    print("\n=== Tickets ===")
    for row in cur.execute("SELECT * FROM ticket;"):
        print(row)

    print("\n=== Crew Members ===")
    for row in cur.execute("SELECT * FROM crew_member;"):
        print(row)

    print("\n=== Crew Assignments ===")
    for row in cur.execute("""
        SELECT ca.id, cm.name, cm.role, f.code, ca.duty
        FROM crew_assignment ca
        JOIN crew_member cm ON ca.crew_member_id=cm.id
        JOIN flight f ON ca.flight_id=f.id
    """):
        print(row)

    print("\n=== Users (roles only) ===")
    for row in cur.execute("SELECT username, role FROM user;"):
        print(row)


if __name__ == "__main__":
    conn = sqlite3.connect(DB_FILE)
    seed_data(conn)
    run_queries(conn)
    conn.close()
