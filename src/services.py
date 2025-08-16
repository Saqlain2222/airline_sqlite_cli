from .dal import DAL
from .config import DB_PATH


class Services:
    def __init__(self, db_path: str = DB_PATH):
        self.dal = DAL(db_path)

    # ----------------------------
    # Passengers
    # ----------------------------
    def add_passenger(self, name: str, email: str) -> int:
        return self.dal.create_passenger(name, email)

    def list_passengers(self):
        return list(self.dal.list_passengers())

    # ----------------------------
    # Flights
    # ----------------------------
    def add_flight(self, code, dep_code, arr_code, dep_time, arr_time, aircraft_model, base_price):
        return self.dal.create_flight(code, dep_code, arr_code, dep_time, arr_time, aircraft_model, base_price)

    def list_flights(self):
        return list(self.dal.list_flights())

    # ----------------------------
    # Bookings (business logic applied)
    # ----------------------------
    def book(self, passenger_id: int, flight_id: int, price: float, cls: str = "ECONOMY") -> dict:
        # Count current tickets for flight
        used = self.dal.count_tickets_for_flight(flight_id)
        cap = self.dal.aircraft_capacity_for_flight(flight_id)

        if used >= cap:
            raise ValueError("Flight is already full, cannot book.")

        # Create booking
        booking_id = self.dal.create_booking(passenger_id, flight_id, price)

        # Auto-generate seat number and ticket number
        seat_no = f"S{used+1:03d}"       # e.g. S001
        ticket_no = f"T{booking_id:06d}"  # e.g. T000001

        ticket_id = self.dal.issue_ticket(booking_id, ticket_no, seat_no, cls)

        return {
            "booking_id": booking_id,
            "ticket_id": ticket_id,
            "seat_no": seat_no,
            "ticket_no": ticket_no,
            "status": "BOOKED",
        }

    def cancel_booking(self, booking_id: int):
        self.dal.cancel_booking(booking_id)

    def bookings_for_passenger(self, passenger_id: int):
        return list(self.dal.list_bookings_by_passenger(passenger_id))

    def all_bookings(self):
        return list(self.dal.list_all_bookings())
