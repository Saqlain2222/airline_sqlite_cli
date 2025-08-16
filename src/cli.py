import argparse
from pprint import pprint
from . import db
from .services import Services
from .config import DB_PATH
from .analytics import Analytics


def _svc():
    return Services(DB_PATH)

def _analytics():
    return Analytics(DB_PATH)


# ----------------------------
# Commands
# ----------------------------
def cmd_init_db(_):
    db.apply_schema(DB_PATH)
    print("Schema applied.")

def cmd_seed(_):
    db.seed_demo(DB_PATH)
    print("Demo data inserted.")

def cmd_add_passenger(args):
    pid = _svc().add_passenger(args.name, args.email)
    print(f"Passenger created with id={pid}")

def cmd_list_passengers(_):
    passengers = _svc().list_passengers()
    print("=== Passengers ===")
    if not passengers:
        print("No passengers found.")
    else:
        pprint(passengers)

def cmd_list_flights(_):
    flights = _svc().list_flights()
    print("=== Flights ===")
    if not flights:
        print("No flights found.")
    else:
        pprint(flights)

def cmd_book(args):
    svc = _svc()

    # 1. Lookup passenger by email
    passenger = svc.dal.get_passenger_by_email(args.email)
    if not passenger:
        print(f"No passenger with email {args.email} found.")
        return

    # 2. Lookup flight by code
    flights = [f for f in svc.dal.list_flights() if f["code"] == args.flight_code]
    if not flights:
        print(f"No flight with code {args.flight_code} found.")
        return
    flight = flights[0]

    # 3. Price: use provided or default to flight’s base price
    price = args.price if args.price else flight["base_price"]

    # 4. Create booking
    booking = svc.book(passenger["id"], flight["id"], price, args.cls)
    print("Booking successful:")
    pprint(booking)

def cmd_list_bookings(args):
    if args.passenger_email:
        passenger = _svc().dal.get_passenger_by_email(args.passenger_email)
        if not passenger:
            print(f"No passenger with email {args.passenger_email} found.")
            return
        bookings = _svc().bookings_for_passenger(passenger["id"])
    else:
        bookings = _svc().all_bookings()

    print("=== Bookings ===")
    if not bookings:
        print("No bookings found.")
    else:
        pprint(bookings)


# ----------------------------
# Analytics Commands
# ----------------------------
def cmd_top_routes(args):
    res = _analytics().top_routes(limit=args.limit)
    print("Top Routes by Passenger Volume")
    if not res:
        print("No data found. Did you book any flights?")
    else:
        pprint(res)

def cmd_revenue_by_month(_):
    res = _analytics().revenue_by_month()
    print("Monthly Revenue")
    if not res:
        print("No revenue data. Try booking a flight first.")
    else:
        pprint(res)

def cmd_load_factor(_):
    res = _analytics().load_factor()
    print("Load Factor per Flight")
    if not res:
        print("No flights/tickets found.")
    else:
        pprint(res)

def cmd_revenue_by_flight(_):
    res = _analytics().revenue_by_flight()
    print("Revenue by Flight")
    if not res:
        print("No revenue data yet.")
    else:
        pprint(res)


# ----------------------------
# CLI Parser
# ----------------------------
def build_parser():
    parser = argparse.ArgumentParser(description="Airline SQLite CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # DB setup
    sub.add_parser("init-db").set_defaults(func=cmd_init_db)
    sub.add_parser("seed").set_defaults(func=cmd_seed)

    # Core functionality
    p = sub.add_parser("add-passenger")
    p.add_argument("--name", required=True)
    p.add_argument("--email", required=True)
    p.set_defaults(func=cmd_add_passenger)

    sub.add_parser("list-passengers").set_defaults(func=cmd_list_passengers)
    sub.add_parser("list-flights").set_defaults(func=cmd_list_flights)

    # Book by email + flight code
    p = sub.add_parser("book", help="Book a passenger onto a flight")
    p.add_argument("--email", required=True, help="Passenger email")
    p.add_argument("--flight-code", required=True, help="Flight code")
    p.add_argument("--price", type=float, help="Optional price override")
    p.add_argument("--class", dest="cls", choices=["ECONOMY","BUSINESS","FIRST"], default="ECONOMY")
    p.set_defaults(func=cmd_book)

    # List bookings
    p = sub.add_parser("list-bookings")
    p.add_argument("--passenger-email", help="Optional filter by passenger email")
    p.set_defaults(func=cmd_list_bookings)

    # Analytics
    p = sub.add_parser("top-routes")
    p.add_argument("--limit", type=int, default=5)
    p.set_defaults(func=cmd_top_routes)

    sub.add_parser("revenue-by-month").set_defaults(func=cmd_revenue_by_month)
    sub.add_parser("load-factor").set_defaults(func=cmd_load_factor)
    sub.add_parser("revenue-by-flight").set_defaults(func=cmd_revenue_by_flight)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
