from typing import Optional, Iterable
from .db import connect
from .config import DB_PATH


class DAL:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    # ----------------------------
    # Passengers
    # ----------------------------
    def create_passenger(self, name: str, email: str) -> int:
        with connect(self.db_path) as conn:
            cur = conn.execute(
                "INSERT INTO passenger(name, email) VALUES (?, ?)",
                (name, email),
            )
            return cur.lastrowid

    def get_passenger_by_email(self, email: str) -> Optional[dict]:
        with connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT * FROM passenger WHERE email = ?", (email,)
            ).fetchone()
            return dict(row) if row else None

    def list_passengers(self) -> Iterable[dict]:
        with connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT id, name, email FROM passenger ORDER BY id"
            ).fetchall()
            for r in rows:
                yield dict(r)

    # ----------------------------
    # Flights
    # ----------------------------
    def create_flight(
        self,
        code: str,
        dep_code: str,
        arr_code: str,
        dep_time: str,
        arr_time: str,
        aircraft_model: str,
        base_price: float,
    ) -> int:
        with connect(self.db_path) as conn:
            cur = conn.execute(
                """
                INSERT INTO flight(code, departure_airport_id, arrival_airport_id,
                                   departure_time, arrival_time, aircraft_id, base_price)
                VALUES (
                    ?, 
                    (SELECT id FROM airport WHERE code=?),
                    (SELECT id FROM airport WHERE code=?),
                    ?, ?, 
                    (SELECT id FROM aircraft WHERE model=?),
                    ?
                )
                """,
                (code, dep_code, arr_code, dep_time, arr_time, aircraft_model, base_price),
            )
            return cur.lastrowid

    def list_flights(self) -> Iterable[dict]:
        with connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT f.id, f.code, dep.code AS dep, arr.code AS arr,
                       f.departure_time, f.arrival_time, a.model AS aircraft, f.base_price
                FROM flight f
                JOIN airport dep ON dep.id = f.departure_airport_id
                JOIN airport arr ON arr.id = f.arrival_airport_id
                JOIN aircraft a ON a.id = f.aircraft_id
                ORDER BY datetime(f.departure_time)
                """
            ).fetchall()
            for row in rows:
                yield dict(row)

    # ----------------------------
    # Bookings
    # ----------------------------
    def create_booking(self, passenger_id: int, flight_id: int, price: float) -> int:
        with connect(self.db_path) as conn:
            cur = conn.execute(
                "INSERT INTO booking(passenger_id, flight_id, status, price) VALUES (?, ?, 'BOOKED', ?)",
                (passenger_id, flight_id, price),
            )
            return cur.lastrowid

    def cancel_booking(self, booking_id: int) -> None:
        with connect(self.db_path) as conn:
            conn.execute("UPDATE booking SET status='CANCELLED' WHERE id=?", (booking_id,))

    def list_bookings_by_passenger(self, passenger_id: int) -> Iterable[dict]:
        with connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT b.id AS booking_id, b.status, b.booked_at, b.price,
                       f.code AS flight_code, f.departure_time, f.arrival_time
                FROM booking b
                JOIN flight f ON f.id = b.flight_id
                WHERE b.passenger_id = ?
                ORDER BY datetime(b.booked_at) DESC
                """,
                (passenger_id,),
            ).fetchall()
            for r in rows:
                yield dict(r)

    def list_all_bookings(self) -> Iterable[dict]:
        """Return all bookings with passenger and flight details."""
        with connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT b.id AS booking_id,
                       p.name AS passenger_name,
                       f.code AS flight_code,
                       f.departure_time,
                       f.arrival_time,
                       b.price,
                       b.status,
                       b.booked_at
                FROM booking b
                JOIN passenger p ON b.passenger_id = p.id
                JOIN flight f ON b.flight_id = f.id
                ORDER BY datetime(b.booked_at) DESC
                """
            ).fetchall()
            for r in rows:
                yield dict(r)

    # ----------------------------
    # Tickets
    # ----------------------------
    def issue_ticket(self, booking_id: int, ticket_no: str, seat_no: str, cls: str) -> int:
        with connect(self.db_path) as conn:
            cur = conn.execute(
                "INSERT INTO ticket(booking_id, ticket_no, seat_no, class) VALUES (?, ?, ?, ?)",
                (booking_id, ticket_no, seat_no, cls),
            )
            return cur.lastrowid

    def tickets_for_booking(self, booking_id: int) -> Iterable[dict]:
        with connect(self.db_path) as conn:
            rows = conn.execute("SELECT * FROM ticket WHERE booking_id=?", (booking_id,)).fetchall()
            for r in rows:
                yield dict(r)

    # ----------------------------
    # Helpers for business logic
    # ----------------------------
    def count_tickets_for_flight(self, flight_id: int) -> int:
        with connect(self.db_path) as conn:
            row = conn.execute(
                """
                SELECT COUNT(t.id) AS n
                FROM ticket t
                JOIN booking b ON b.id = t.booking_id
                WHERE b.flight_id = ? AND b.status = 'BOOKED'
                """,
                (flight_id,),
            ).fetchone()
            return int(row["n"])

    def aircraft_capacity_for_flight(self, flight_id: int) -> int:
        with connect(self.db_path) as conn:
            row = conn.execute(
                """
                SELECT a.capacity AS cap
                FROM flight f
                JOIN aircraft a ON a.id = f.aircraft_id
                WHERE f.id = ?
                """,
                (flight_id,),
            ).fetchone()
            return int(row["cap"])
