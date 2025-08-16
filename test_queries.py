import sqlite3
from datetime import datetime

DB_FILE = "airline.db"

def seed_data(conn):
    cur = conn.cursor()

    # Clear existing data
    cur.executescript("""
    DELETE FROM ticket;
    DELETE FROM booking;
    DELETE FROM flight;
    DELETE FROM passenger;
    DELETE FROM aircraft;
    DELETE FROM airport;
    """)

    # Airports
    cur.executemany("""
    INSERT INTO airport (code, name, city, country)
    VALUES (?, ?, ?, ?)
    """, [
        ("LHR", "Heathrow", "London", "UK"),
        ("JFK", "John F. Kennedy Intl", "New York", "United States"),
        ("SYD", "Sydney Intl", "Sydney", "Australia")
    ])

    # Aircraft
    cur.executemany("""
    INSERT INTO aircraft (model, capacity)
    VALUES (?, ?)
    """, [
        ("Airbus A320", 180),
        ("Boeing 777-300ER", 396)
    ])

    # Passengers
    cur.executemany("""
    INSERT INTO passenger (name, email)
    VALUES (?, ?)
    """, [
        ("John Smith", "john.smith@example.com"),
        ("Emily Johnson", "emily.johnson@example.com"),
        ("Michael Brown", "michael.brown@example.com"),
        ("Sarah Wilson", "sarah.wilson@example.com")
    ])

    # Flights
    cur.executemany("""
    INSERT INTO flight (code, departure_airport_id, arrival_airport_id,
                        departure_time, arrival_time, aircraft_id, base_price)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        ("BA101", 1, 2, "2025-09-01T08:00:00", "2025-09-01T11:00:00", 1, 250.0),
        ("QF202", 2, 3, "2025-09-02T14:00:00", "2025-09-03T08:00:00", 2, 900.0)
    ])

    # Bookings
    cur.executemany("""
    INSERT INTO booking (passenger_id, flight_id, status, booked_at, price)
    VALUES (?, ?, 'BOOKED', ?, ?)
    """, [
        (1, 1, datetime.now().isoformat(), 260.0),  # John Smith on BA101
        (2, 1, datetime.now().isoformat(), 250.0),  # Emily Johnson on BA101
        (3, 2, datetime.now().isoformat(), 950.0)   # Michael Brown on QF202
    ])

    # Tickets
    cur.executemany("""
    INSERT INTO ticket (booking_id, ticket_no, seat_no, class)
    VALUES (?, ?, ?, ?)
    """, [
        (1, "T000001", "12A", "ECONOMY"),
        (2, "T000002", "14C", "ECONOMY"),
        (3, "T000003", "3B", "BUSINESS")
    ])

    conn.commit()


def run_queries(conn):
    cur = conn.cursor()

    print("\n=== Passengers ===")
    for row in cur.execute("SELECT * FROM passenger;"):
        print(row)

    print("\n=== Flights ===")
    for row in cur.execute("""
        SELECT f.code, a1.code, a2.code, f.departure_time, f.arrival_time
        FROM flight f
        JOIN airport a1 ON f.departure_airport_id = a1.id
        JOIN airport a2 ON f.arrival_airport_id = a2.id
    """):
        print(row)

    print("\n=== Bookings with Passengers ===")
    for row in cur.execute("""
        SELECT b.id, p.name, f.code, b.price
        FROM booking b
        JOIN passenger p ON b.passenger_id = p.id
        JOIN flight f ON b.flight_id = f.id
    """):
        print(row)

    print("\n=== Revenue by Flight ===")
    for row in cur.execute("""
        SELECT f.code, SUM(b.price) AS total_revenue
        FROM booking b
        JOIN flight f ON b.flight_id = f.id
        GROUP BY f.code
    """):
        print(row)


if __name__ == "__main__":
    conn = sqlite3.connect(DB_FILE)
    seed_data(conn)
    run_queries(conn)
    conn.close()
