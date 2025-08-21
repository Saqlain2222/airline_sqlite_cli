import sqlite3
from pathlib import Path

DB_PATH = "airline.db"


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def cleanup_duplicates(conn):
    cur = conn.cursor()

    # Aircraft duplicates
    cur.execute("""
        DELETE FROM aircraft
        WHERE id NOT IN (
          SELECT MIN(id)
          FROM aircraft
          GROUP BY model, capacity
        )
    """)

    # Booking duplicates
    cur.execute("""
        DELETE FROM booking
        WHERE id NOT IN (
          SELECT MIN(id)
          FROM booking
          GROUP BY passenger_id, flight_id
        )
    """)

    # Crew assignment duplicates
    cur.execute("""
        DELETE FROM crew_assignment
        WHERE id NOT IN (
          SELECT MIN(id)
          FROM crew_assignment
          GROUP BY crew_member_id, flight_id
        )
    """)

    conn.commit()
    print("Duplicate cleanup done.")


def apply_constraints_and_indexes(conn):
    cur = conn.cursor()
    cur.executescript("""
        PRAGMA foreign_keys = OFF;
        BEGIN TRANSACTION;

        -- ========================
        -- Enforce UNIQUE constraints
        -- ========================
        CREATE UNIQUE INDEX IF NOT EXISTS uq_aircraft_model_capacity
            ON aircraft(model, capacity);

        CREATE UNIQUE INDEX IF NOT EXISTS uq_booking_passenger_flight
            ON booking(passenger_id, flight_id);

        CREATE UNIQUE INDEX IF NOT EXISTS uq_crew_assignment_member_flight
            ON crew_assignment(crew_member_id, flight_id);

        CREATE UNIQUE INDEX IF NOT EXISTS uq_ticket_no
            ON ticket(ticket_no);

        CREATE UNIQUE INDEX IF NOT EXISTS uq_user_username
            ON user(username);

        CREATE UNIQUE INDEX IF NOT EXISTS uq_passenger_email
            ON passenger(email);

        CREATE UNIQUE INDEX IF NOT EXISTS uq_flight_code
            ON flight(code);

        -- ========================
        -- Supporting performance indexes
        -- ========================
        CREATE INDEX IF NOT EXISTS idx_flight_dep_arr_date
          ON flight (departure_airport_id, arrival_airport_id, date(departure_time));

        CREATE INDEX IF NOT EXISTS idx_booking_passenger
          ON booking (passenger_id);

        CREATE INDEX IF NOT EXISTS idx_booking_flight
          ON booking (flight_id, passenger_id);

        CREATE INDEX IF NOT EXISTS idx_ticket_booking
          ON ticket (booking_id);

        CREATE INDEX IF NOT EXISTS idx_crew_assignment_flight
          ON crew_assignment (flight_id);

        COMMIT;
        PRAGMA foreign_keys = ON;
    """)
    print("Indexes & constraints applied.")


def main():
    with connect() as conn:
        cleanup_duplicates(conn)
        apply_constraints_and_indexes(conn)

    print("Migration completed successfully.")


if __name__ == "__main__":
    main()
