from typing import Iterable, Dict
from .db import connect
from .config import DB_PATH


class Analytics:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    # 1. Top routes by passenger volume
    def top_routes(self, limit: int = 5) -> Iterable[Dict]:
        with connect(self.db_path) as conn:
            rows = conn.execute("""
                SELECT dep.code || ' → ' || arr.code AS route,
                       COUNT(b.id) AS bookings
                FROM booking b
                JOIN flight f ON b.flight_id = f.id
                JOIN airport dep ON dep.id = f.departure_airport_id
                JOIN airport arr ON arr.id = f.arrival_airport_id
                WHERE b.status = 'BOOKED'
                GROUP BY route
                ORDER BY bookings DESC
                LIMIT ?
            """, (limit,)).fetchall()
            return [dict(r) for r in rows]

    # 2. Monthly revenue totals
    def revenue_by_month(self) -> Iterable[Dict]:
        with connect(self.db_path) as conn:
            rows = conn.execute("""
                SELECT strftime('%Y-%m', booked_at) AS month,
                       SUM(price) AS total_revenue
                FROM booking
                WHERE status = 'BOOKED'
                GROUP BY month
                ORDER BY month ASC
            """).fetchall()
            return [dict(r) for r in rows]

    # 3. Load factor per flight (booked seats / capacity)
    def load_factor(self) -> Iterable[Dict]:
        with connect(self.db_path) as conn:
            rows = conn.execute("""
                SELECT f.code AS flight,
                       COALESCE(COUNT(t.id) * 1.0 / a.capacity, 0) AS load_factor
                FROM flight f
                JOIN aircraft a ON f.aircraft_id = a.id
                LEFT JOIN booking b ON f.id = b.flight_id AND b.status='BOOKED'
                LEFT JOIN ticket t ON b.id = t.booking_id
                GROUP BY f.id
                ORDER BY load_factor DESC
            """).fetchall()
            return [dict(r) for r in rows]

    # 4. Revenue by flight
    def revenue_by_flight(self) -> Iterable[Dict]:
        with connect(self.db_path) as conn:
            rows = conn.execute("""
                SELECT f.code AS flight,
                       SUM(b.price) AS revenue
                FROM booking b
                JOIN flight f ON b.flight_id = f.id
                WHERE b.status = 'BOOKED'
                GROUP BY f.code
                ORDER BY revenue DESC
            """).fetchall()
            return [dict(r) for r in rows]
