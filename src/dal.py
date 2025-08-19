import sqlite3
from sqlite3 import connect
from datetime import datetime
import uuid, random


class DAL:
    def __init__(self, db_path="airline.db"):
        self.db_path = db_path

    # ----------------------------
    # Passenger CRUD
    # ----------------------------
    def create_passenger(self, name, email):
        with connect(self.db_path) as conn:
            cur = conn.execute(
                "INSERT INTO passenger (name, email) VALUES (?, ?)",
                (name, email)
            )
            conn.commit()
            return cur.lastrowid

    def list_passengers(self):
        with connect(self.db_path) as conn:
            cur = conn.execute("SELECT id, name, email FROM passenger")
            return [dict(id=row[0], name=row[1], email=row[2]) for row in cur.fetchall()]

    def update_passenger(self, passenger_id, name=None, email=None):
        with connect(self.db_path) as conn:
            row = conn.execute("SELECT id, name, email FROM passenger WHERE id=?", (passenger_id,)).fetchone()
            if not row:
                return None
            new_name = name if name else row[1]
            new_email = email if email else row[2]
            conn.execute(
                "UPDATE passenger SET name=?, email=? WHERE id=?",
                (new_name, new_email, passenger_id)
            )
            conn.commit()
            return dict(id=passenger_id, name=new_name, email=new_email)

    def delete_passenger(self, passenger_id):
        with connect(self.db_path) as conn:
            cur = conn.execute("DELETE FROM passenger WHERE id=?", (passenger_id,))
            conn.commit()
            return cur.rowcount > 0

    # ----------------------------
    # Airport CRUD
    # ----------------------------
    def create_airport(self, code, name, city, country):
        with connect(self.db_path) as conn:
            cur = conn.execute(
                "INSERT INTO airport (code, name, city, country) VALUES (?, ?, ?, ?)",
                (code, name, city, country)
            )
            conn.commit()
            return cur.lastrowid

    def list_airports(self):
        with connect(self.db_path) as conn:
            cur = conn.execute("SELECT * FROM airport")
            return [dict(id=row[0], code=row[1], name=row[2], city=row[3], country=row[4]) for row in cur.fetchall()]

    def update_airport(self, airport_id, code=None, name=None, city=None, country=None):
        with connect(self.db_path) as conn:
            row = conn.execute("SELECT * FROM airport WHERE id=?", (airport_id,)).fetchone()
            if not row:
                return None
            new_code = code or row[1]
            new_name = name or row[2]
            new_city = city or row[3]
            new_country = country or row[4]
            conn.execute("UPDATE airport SET code=?, name=?, city=?, country=? WHERE id=?",
                         (new_code, new_name, new_city, new_country, airport_id))
            conn.commit()
            return dict(id=airport_id, code=new_code, name=new_name, city=new_city, country=new_country)

    def delete_airport(self, airport_id):
        with connect(self.db_path) as conn:
            cur = conn.execute("DELETE FROM airport WHERE id=?", (airport_id,))
            conn.commit()
            return cur.rowcount > 0

    # ----------------------------
    # Aircraft CRUD
    # ----------------------------
    def create_aircraft(self, model, capacity):
        with connect(self.db_path) as conn:
            cur = conn.execute("INSERT INTO aircraft (model, capacity) VALUES (?, ?)", (model, capacity))
            conn.commit()
            return cur.lastrowid

    def list_aircraft(self):
        with connect(self.db_path) as conn:
            cur = conn.execute("SELECT * FROM aircraft")
            return [dict(id=row[0], model=row[1], capacity=row[2]) for row in cur.fetchall()]

    def update_aircraft(self, aircraft_id, model=None, capacity=None):
        with connect(self.db_path) as conn:
            row = conn.execute("SELECT * FROM aircraft WHERE id=?", (aircraft_id,)).fetchone()
            if not row:
                return None
            new_model = model or row[1]
            new_capacity = capacity or row[2]
            conn.execute("UPDATE aircraft SET model=?, capacity=? WHERE id=?", (new_model, new_capacity, aircraft_id))
            conn.commit()
            return dict(id=aircraft_id, model=new_model, capacity=new_capacity)

    def delete_aircraft(self, aircraft_id):
        with connect(self.db_path) as conn:
            cur = conn.execute("DELETE FROM aircraft WHERE id=?", (aircraft_id,))
            conn.commit()
            return cur.rowcount > 0

    # ----------------------------
    # Flight CRUD
    # ----------------------------
    def create_flight(self, code, departure_airport_id, arrival_airport_id, dep_time, arr_time, aircraft_id, base_price):
        with connect(self.db_path) as conn:
            cur = conn.execute(
                """INSERT INTO flight 
                   (code, departure_airport_id, arrival_airport_id, departure_time, arrival_time, aircraft_id, base_price)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (code, departure_airport_id, arrival_airport_id, dep_time, arr_time, aircraft_id, base_price)
            )
            conn.commit()
            return cur.lastrowid

    def list_flights(self):
        with connect(self.db_path) as conn:
            cur = conn.execute("SELECT * FROM flight")
            return [dict(
                id=row[0], code=row[1],
                departure_airport_id=row[2], arrival_airport_id=row[3],
                departure_time=row[4], arrival_time=row[5],
                aircraft_id=row[6], base_price=row[7]
            ) for row in cur.fetchall()]

    def update_flight(self, flight_id, code=None, departure_airport_id=None, arrival_airport_id=None,
                      departure_time=None, arrival_time=None, aircraft_id=None, base_price=None):
        with connect(self.db_path) as conn:
            row = conn.execute("SELECT * FROM flight WHERE id=?", (flight_id,)).fetchone()
            if not row:
                return None
            new_code = code or row[1]
            new_dep_airport = departure_airport_id or row[2]
            new_arr_airport = arrival_airport_id or row[3]
            new_departure = departure_time or row[4]
            new_arrival = arrival_time or row[5]
            new_aircraft = aircraft_id or row[6]
            new_price = base_price or row[7]
            conn.execute("""UPDATE flight 
                            SET code=?, departure_airport_id=?, arrival_airport_id=?, 
                                departure_time=?, arrival_time=?, aircraft_id=?, base_price=? 
                            WHERE id=?""",
                         (new_code, new_dep_airport, new_arr_airport, new_departure,
                          new_arrival, new_aircraft, new_price, flight_id))
            conn.commit()
            return dict(id=flight_id, code=new_code, departure_airport_id=new_dep_airport,
                        arrival_airport_id=new_arr_airport, departure_time=new_departure,
                        arrival_time=new_arrival, aircraft_id=new_aircraft, base_price=new_price)

    def delete_flight(self, flight_id):
        with connect(self.db_path) as conn:
            cur = conn.execute("DELETE FROM flight WHERE id=?", (flight_id,))
            conn.commit()
            return cur.rowcount > 0

    # ----------------------------
    # Booking + Ticket
    # ----------------------------
    def create_booking(self, passenger_id, flight_id, ticket_class, price, seat_no=None):
        with connect(self.db_path) as conn:
            cur = conn.execute(
                "INSERT INTO booking (passenger_id, flight_id, status, booked_at, price) VALUES (?, ?, 'CONFIRMED', ?, ?)",
                (passenger_id, flight_id, datetime.utcnow().isoformat(), price)
            )
            booking_id = cur.lastrowid
            ticket_no = str(uuid.uuid4())[:8].upper()
            if not seat_no:
                seat_no = f"{random.randint(1,30)}{chr(random.randint(65,70))}"
            conn.execute(
                "INSERT INTO ticket (booking_id, ticket_no, seat_no, class) VALUES (?, ?, ?, ?)",
                (booking_id, ticket_no, seat_no, ticket_class)
            )
            conn.commit()
            return booking_id

    def list_bookings(self):
        with connect(self.db_path) as conn:
            cur = conn.execute("""SELECT b.id, b.passenger_id, b.flight_id, b.status, b.booked_at, b.price,
                                         t.ticket_no, t.seat_no, t.class
                                  FROM booking b LEFT JOIN ticket t ON b.id = t.booking_id""")
            return [dict(id=row[0], passenger_id=row[1], flight_id=row[2], status=row[3],
                         booked_at=row[4], price=row[5], ticket_no=row[6], seat_no=row[7], ticket_class=row[8])
                    for row in cur.fetchall()]

    def update_booking(self, booking_id, status=None, price=None):
        with connect(self.db_path) as conn:
            row = conn.execute("SELECT * FROM booking WHERE id=?", (booking_id,)).fetchone()
            if not row:
                return None
            new_status = status or row[3]
            new_price = price or row[5]
            conn.execute("UPDATE booking SET status=?, price=? WHERE id=?", (new_status, new_price, booking_id))
            conn.commit()
            return dict(id=booking_id, passenger_id=row[1], flight_id=row[2], status=new_status, price=new_price)

    def delete_booking(self, booking_id):
        with connect(self.db_path) as conn:
            conn.execute("DELETE FROM ticket WHERE booking_id=?", (booking_id,))
            cur = conn.execute("DELETE FROM booking WHERE id=?", (booking_id,))
            conn.commit()
            return cur.rowcount > 0

    # ----------------------------
    # Crew Member CRUD
    # ----------------------------
    def create_crew_member(self, name, role):
        with connect(self.db_path) as conn:
            cur = conn.execute("INSERT INTO crew_member (name, role) VALUES (?, ?)", (name, role))
            conn.commit()
            return cur.lastrowid

    def list_crew_members(self):
        with connect(self.db_path) as conn:
            cur = conn.execute("SELECT * FROM crew_member")
            return [dict(id=row[0], name=row[1], role=row[2]) for row in cur.fetchall()]

    def update_crew_member(self, crew_id, name=None, role=None):
        with connect(self.db_path) as conn:
            row = conn.execute("SELECT * FROM crew_member WHERE id=?", (crew_id,)).fetchone()
            if not row:
                return None
            new_name = name or row[1]
            new_role = role or row[2]
            conn.execute("UPDATE crew_member SET name=?, role=? WHERE id=?", (new_name, new_role, crew_id))
            conn.commit()
            return dict(id=crew_id, name=new_name, role=new_role)

    def delete_crew_member(self, crew_id):
        with connect(self.db_path) as conn:
            cur = conn.execute("DELETE FROM crew_member WHERE id=?", (crew_id,))
            conn.commit()
            return cur.rowcount > 0

    # ----------------------------
    # Crew Assignment CRUD
    # ----------------------------
    def create_crew_assignment(self, crew_member_id, flight_id, duty):
        with connect(self.db_path) as conn:
            cur = conn.execute("INSERT INTO crew_assignment (crew_member_id, flight_id, duty) VALUES (?, ?, ?)",
                               (crew_member_id, flight_id, duty))
            conn.commit()
            return cur.lastrowid

    def list_crew_assignments(self):
        with connect(self.db_path) as conn:
            cur = conn.execute("SELECT * FROM crew_assignment")
            return [dict(id=row[0], crew_member_id=row[1], flight_id=row[2], duty=row[3]) for row in cur.fetchall()]

    def update_crew_assignment(self, assignment_id, crew_member_id=None, flight_id=None, duty=None):
        with connect(self.db_path) as conn:
            row = conn.execute("SELECT * FROM crew_assignment WHERE id=?", (assignment_id,)).fetchone()
            if not row:
                return None
            new_crew = crew_member_id or row[1]
            new_flight = flight_id or row[2]
            new_duty = duty or row[3]
            conn.execute("UPDATE crew_assignment SET crew_member_id=?, flight_id=?, duty=? WHERE id=?",
                         (new_crew, new_flight, new_duty, assignment_id))
            conn.commit()
            return dict(id=assignment_id, crew_member_id=new_crew, flight_id=new_flight, duty=new_duty)

    def delete_crew_assignment(self, assignment_id):
        with connect(self.db_path) as conn:
            cur = conn.execute("DELETE FROM crew_assignment WHERE id=?", (assignment_id,))
            conn.commit()
            return cur.rowcount > 0

    # ----------------------------
    # User CRUD
    # ----------------------------

    def create_user(self, username, password_hash, salt, role):
            with connect(self.db_path) as conn:
                cur = conn.execute(
                    "INSERT INTO user (username, password_hash, salt, role) VALUES (?, ?, ?, ?)",
                    (username, password_hash, salt, role.upper())
                    # force upper if your schema expects ADMIN/STAFF/CUSTOMER
                )
                conn.commit()
                return cur.lastrowid

    def list_users(self):
            with connect(self.db_path) as conn:
                cur = conn.execute("SELECT id, username, role FROM user")
                return [dict(id=row[0], username=row[1], role=row[2]) for row in cur.fetchall()]

    def update_user(self, user_id, username=None, password_hash=None, salt=None, role=None):
            with connect(self.db_path) as conn:
                row = conn.execute("SELECT * FROM user WHERE id=?", (user_id,)).fetchone()
                if not row:
                    return None

                new_username = username or row[1]
                new_password_hash = password_hash or row[2]
                new_salt = salt or row[3]
                new_role = role.upper() if role else row[4]

                conn.execute(
                    "UPDATE user SET username=?, password_hash=?, salt=?, role=? WHERE id=?",
                    (new_username, new_password_hash, new_salt, new_role, user_id)
                )
                conn.commit()
                return dict(id=user_id, username=new_username, role=new_role)

    def delete_user(self, user_id):
            with connect(self.db_path) as conn:
                cur = conn.execute("DELETE FROM user WHERE id=?", (user_id,))
                conn.commit()
                return cur.rowcount > 0

    # ----------------------------
    # Ticket CRUD
    # ----------------------------
    def create_ticket(self, booking_id, ticket_no, seat_no, ticket_class):
        with connect(self.db_path) as conn:
            cur = conn.execute(
                "INSERT INTO ticket (booking_id, ticket_no, seat_no, class) VALUES (?, ?, ?, ?)",
                (booking_id, ticket_no, seat_no, ticket_class)
            )
            conn.commit()
            return cur.lastrowid

    def list_tickets(self):
        with connect(self.db_path) as conn:
            cur = conn.execute("SELECT * FROM ticket")
            return [dict(id=row[0], booking_id=row[1], ticket_no=row[2], seat_no=row[3], ticket_class=row[4]) for row in cur.fetchall()]

    def update_ticket(self, ticket_id, ticket_no=None, seat_no=None, ticket_class=None):
        with connect(self.db_path) as conn:
            row = conn.execute("SELECT * FROM ticket WHERE id=?", (ticket_id,)).fetchone()
            if not row:
                return None
            new_ticket_no = ticket_no or row[2]
            new_seat_no = seat_no or row[3]
            new_class = ticket_class or row[4]
            conn.execute("UPDATE ticket SET ticket_no=?, seat_no=?, class=? WHERE id=?",
                         (new_ticket_no, new_seat_no, new_class, ticket_id))
            conn.commit()
            return dict(id=ticket_id, booking_id=row[1], ticket_no=new_ticket_no, seat_no=new_seat_no, ticket_class=new_class)

    def delete_ticket(self, ticket_id):
        with connect(self.db_path) as conn:
            cur = conn.execute("DELETE FROM ticket WHERE id=?", (ticket_id,))
            conn.commit()
            return cur.rowcount > 0

    # ----------------------------
    # Reports / Advanced Queries
    # ----------------------------

    def top_passengers(self, limit=10):
        """Return passengers ranked by most bookings"""
        with connect(self.db_path) as conn:
            cur = conn.execute("""
                SELECT p.id, p.name, p.email, COUNT(b.id) AS total_bookings
                FROM passenger p
                JOIN booking b ON p.id = b.passenger_id
                GROUP BY p.id, p.name, p.email
                ORDER BY total_bookings DESC
                LIMIT ?
            """, (limit,))
            return [dict(id=row[0], name=row[1], email=row[2], total_bookings=row[3]) for row in cur.fetchall()]

    def revenue_rankings(self, limit=10):
        """Return flights ranked by highest revenue"""
        with connect(self.db_path) as conn:
            cur = conn.execute("""
                SELECT f.id, f.code, SUM(b.price) AS total_revenue, COUNT(b.id) AS total_bookings
                FROM flight f
                JOIN booking b ON f.id = b.flight_id
                GROUP BY f.id, f.code
                ORDER BY total_revenue DESC
                LIMIT ?
            """, (limit,))
            return [dict(id=row[0], code=row[1], total_revenue=row[2], total_bookings=row[3]) for row in cur.fetchall()]

    def route_load_factors(self, limit=10):
        """Return routes ranked by load factor (booked seats ÷ aircraft capacity)"""
        with connect(self.db_path) as conn:
            cur = conn.execute("""
                SELECT 
                    f.id, f.code,
                    dep.code AS departure_airport,
                    arr.code AS arrival_airport,
                    a.capacity,
                    COUNT(t.id) AS booked_seats,
                    ROUND(CAST(COUNT(t.id) AS FLOAT) / a.capacity, 2) AS load_factor
                FROM flight f
                JOIN aircraft a ON f.aircraft_id = a.id
                LEFT JOIN booking b ON f.id = b.flight_id
                LEFT JOIN ticket t ON b.id = t.booking_id
                JOIN airport dep ON f.departure_airport_id = dep.id
                JOIN airport arr ON f.arrival_airport_id = arr.id
                GROUP BY f.id, f.code, dep.code, arr.code, a.capacity
                ORDER BY load_factor DESC
                LIMIT ?
            """, (limit,))
            return [dict(
                flight_id=row[0], flight_code=row[1],
                departure=row[2], arrival=row[3],
                capacity=row[4], booked_seats=row[5],
                load_factor=row[6]
            ) for row in cur.fetchall()]
