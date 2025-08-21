import os
import hashlib
from .dal import DAL
from .mongo_dal import MongoDAL  # <-- for Mongo hybrid later

class Services:
    def __init__(self, db_path="airline.db", mongo_uri=None):
        self.dal = DAL(db_path)
        self.mongo = MongoDAL(mongo_uri) if mongo_uri else None

    # ----------------------------
    # Helper: password hashing
    # ----------------------------
    def _hash_password(self, password, salt=None):
        if salt is None:
            salt = os.urandom(16).hex()
        pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return pwd_hash, salt

    # ----------------------------
    # Passenger Services
    # ----------------------------
    def add_passenger(self, name, email):
        return self.dal.create_passenger(name, email)

    def get_passengers(self):
        return self.dal.list_passengers()

    def update_passenger(self, passenger_id, name=None, email=None):
        return self.dal.update_passenger(passenger_id, name, email)

    def delete_passenger(self, passenger_id):
        return self.dal.delete_passenger(passenger_id)

    # ----------------------------
    # Airport Services
    # ----------------------------
    def add_airport(self, code, name, city, country):
        return self.dal.create_airport(code, name, city, country)

    def get_airports(self):
        return self.dal.list_airports()

    def update_airport(self, airport_id, code=None, name=None, city=None, country=None):
        return self.dal.update_airport(airport_id, code, name, city, country)

    def delete_airport(self, airport_id):
        return self.dal.delete_airport(airport_id)

    # ----------------------------
    # Aircraft Services
    # ----------------------------
    def add_aircraft(self, model, capacity):
        return self.dal.create_aircraft(model, capacity)

    def get_aircraft(self):
        return self.dal.list_aircraft()

    def update_aircraft(self, aircraft_id, model=None, capacity=None):
        return self.dal.update_aircraft(aircraft_id, model, capacity)

    def delete_aircraft(self, aircraft_id):
        return self.dal.delete_aircraft(aircraft_id)

    # ----------------------------
    # Flight Services
    # ----------------------------
    def add_flight(self, code, origin, destination, departure, arrival, aircraft, price):
        return self.dal.create_flight(code, origin, destination, departure, arrival, aircraft, price)

    def get_flights(self):
        return self.dal.list_flights()

    def update_flight(self, flight_id, **kwargs):
        return self.dal.update_flight(flight_id, **kwargs)

    def delete_flight(self, flight_id):
        return self.dal.delete_flight(flight_id)

    # ----------------------------
    # Booking + Ticket Services
    # ----------------------------
    def book(self, passenger_id, flight_id, ticket_class, price, seat_no=None):
        return self.dal.create_booking(passenger_id, flight_id, ticket_class, price, seat_no)

    def get_bookings(self):
        return self.dal.list_bookings()

    def update_booking(self, booking_id, status=None, price=None):
        return self.dal.update_booking(booking_id, status, price)

    def cancel_booking(self, booking_id):
        return self.dal.delete_booking(booking_id)

    # ----------------------------
    # Crew Member Services
    # ----------------------------
    def add_crew_member(self, name, role):
        return self.dal.create_crew_member(name, role)

    def get_crew_members(self):
        return self.dal.list_crew_members()

    def update_crew_member(self, crew_id, name=None, role=None):
        return self.dal.update_crew_member(crew_id, name, role)

    def delete_crew_member(self, crew_id):
        return self.dal.delete_crew_member(crew_id)

    # ----------------------------
    # Crew Assignment Services
    # ----------------------------
    def assign_crew(self, crew_member_id, flight_id, duty):
        return self.dal.create_crew_assignment(crew_member_id, flight_id, duty)

    def get_crew_assignments(self):
        return self.dal.list_crew_assignments()

    def update_crew_assignment(self, assignment_id, crew_member_id=None, flight_id=None, duty=None):
        return self.dal.update_crew_assignment(assignment_id, crew_member_id, flight_id, duty)

    def delete_crew_assignment(self, assignment_id):
        return self.dal.delete_crew_assignment(assignment_id)

    # ----------------------------
    # User Services (secure)
    # ----------------------------
    def add_user(self, username, password, role):
        pwd_hash, salt = self._hash_password(password)
        if role:
            role = role.upper()
        return self.dal.create_user(username, pwd_hash, salt, role)

    def get_users(self):
        users = self.dal.list_users()
        # Ensure we don’t expose hashes
        return [{"id": u[0], "username": u[1], "role": u[2]} for u in users]

    def update_user(self, user_id, username=None, password=None, role=None):
        pwd_hash, salt = (None, None)
        if password:
            pwd_hash, salt = self._hash_password(password)
        if role:
            role = role.upper()
        return self.dal.update_user(user_id, username, pwd_hash, salt, role)

    def delete_user(self, user_id):
        return self.dal.delete_user(user_id)

    # ----------------------------
    # Reports (Advanced SQL)
    # ----------------------------
    def top_passengers(self, limit=5):
        """Passengers ranked by number of bookings."""
        return self.dal.query_top_passengers(limit)

    def revenue_rankings(self, limit=5):
        """Flights ranked by total revenue."""
        return self.dal.query_revenue_rankings(limit)

    def route_load(self, limit=5):
        """Routes ranked by load factor (booked seats ÷ aircraft capacity)."""
        return self.dal.query_route_load(limit)

    # ----------------------------
    # Loyalty (MongoDB)
    # ----------------------------
    def add_loyalty_profile(self, passenger_id, tier="Bronze", points=0):
        if not self.mongo:
            raise RuntimeError("MongoDB not configured")
        return self.mongo.create_loyalty_profile(passenger_id, tier, points)

    def get_loyalty_profiles(self):
        if not self.mongo:
            raise RuntimeError("MongoDB not configured")
        return self.mongo.get_loyalty_profiles()

    def add_feedback(self, passenger_id, comment):
        if not self.mongo:
            raise RuntimeError("MongoDB not configured")
        return self.mongo.add_feedback(passenger_id, comment)

    def update_loyalty_points(self, passenger_id, points):
        if not self.mongo:
            raise RuntimeError("MongoDB not configured")
        return self.mongo.update_points(passenger_id, points)

    def delete_loyalty_profile(self, passenger_id):
        if not self.mongo:
            raise RuntimeError("MongoDB not configured")
        return self.mongo.delete_loyalty_profile(passenger_id)
