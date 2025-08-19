import argparse
from pprint import pprint
from .services import Services


def main():
    svc = Services()

    parser = argparse.ArgumentParser(prog="airline-cli")
    subparsers = parser.add_subparsers(dest="command")

    # =========================================================
    # PASSENGER
    # =========================================================
    p = subparsers.add_parser("add-passenger")
    p.add_argument("--name", required=True)
    p.add_argument("--email", required=True)
    p.set_defaults(func=lambda args: print(
        "Passenger created with id",
        svc.add_passenger(args.name, args.email)
    ))

    p = subparsers.add_parser("list-passengers")
    p.set_defaults(func=lambda args: pprint(svc.get_passengers()))

    # =========================================================
    # AIRPORT
    # =========================================================
    a = subparsers.add_parser("add-airport")
    a.add_argument("--code", required=True)
    a.add_argument("--name", required=True)
    a.add_argument("--city", required=True)
    a.add_argument("--country", required=True)
    a.set_defaults(func=lambda args: print(
        "Airport created with id",
        svc.add_airport(args.code, args.name, args.city, args.country)
    ))

    a = subparsers.add_parser("list-airports")
    a.set_defaults(func=lambda args: pprint(svc.get_airports()))

    # =========================================================
    # AIRCRAFT
    # =========================================================
    ac = subparsers.add_parser("add-aircraft")
    ac.add_argument("--model", required=True)
    ac.add_argument("--capacity", type=int, required=True)
    ac.set_defaults(func=lambda args: print(
        "Aircraft created with id",
        svc.add_aircraft(args.model, args.capacity)
    ))

    ac = subparsers.add_parser("list-aircraft")
    ac.set_defaults(func=lambda args: pprint(svc.get_aircraft()))

    # =========================================================
    # FLIGHT
    # =========================================================
    f = subparsers.add_parser("add-flight")
    f.add_argument("--code", required=True)
    f.add_argument("--departure-airport", type=int, required=True)
    f.add_argument("--arrival-airport", type=int, required=True)
    f.add_argument("--departure", required=True)
    f.add_argument("--arrival", required=True)
    f.add_argument("--aircraft-id", type=int, required=True)
    f.add_argument("--price", type=float, required=True)
    f.set_defaults(func=lambda args: print(
        "Flight created with id",
        svc.add_flight(
            args.code, args.departure_airport, args.arrival_airport,
            args.departure, args.arrival, args.aircraft_id, args.price
        )
    ))

    f = subparsers.add_parser("list-flights")
    f.set_defaults(func=lambda args: pprint(svc.get_flights()))

    # =========================================================
    # BOOKING
    # =========================================================
    b = subparsers.add_parser("book")
    b.add_argument("--passenger", type=int, required=True)
    b.add_argument("--flight", type=int, required=True)
    b.add_argument("--class", dest="ticket_class",
                   choices=["ECONOMY", "BUSINESS", "FIRST"], required=True)
    b.add_argument("--price", type=float, required=True)
    b.add_argument("--seat", dest="seat_no", required=False,
                   help="Optional seat number (e.g. 12A)")
    b.set_defaults(func=lambda args: print(
        "Booking created with id",
        svc.book(args.passenger, args.flight,
                 args.ticket_class, args.price, args.seat_no)
    ))

    b = subparsers.add_parser("list-bookings")
    b.set_defaults(func=lambda args: pprint(svc.get_bookings()))

    # =========================================================
    # TICKET
    # =========================================================
    t = subparsers.add_parser("add-ticket")
    t.add_argument("--booking-id", type=int, required=True)
    t.add_argument("--ticket-no", required=True)
    t.add_argument("--seat-no", required=True)
    t.add_argument("--class", dest="ticket_class",
                   choices=["ECONOMY", "BUSINESS", "FIRST"], required=True)
    t.set_defaults(func=lambda args: print(
        "Ticket created with id",
        svc.dal.create_ticket(args.booking_id, args.ticket_no,
                              args.seat_no, args.ticket_class)
    ))

    t = subparsers.add_parser("list-tickets")
    t.set_defaults(func=lambda args: pprint(svc.dal.list_tickets()))

    # =========================================================
    # CREW MEMBER
    # =========================================================
    cm = subparsers.add_parser("add-crew")
    cm.add_argument("--name", required=True)
    cm.add_argument("--role", required=True)
    cm.set_defaults(func=lambda args: print(
        "Crew member created with id",
        svc.add_crew_member(args.name, args.role)
    ))

    cm = subparsers.add_parser("list-crew")
    cm.set_defaults(func=lambda args: pprint(svc.get_crew_members()))

    # =========================================================
    # CREW ASSIGNMENT
    # =========================================================
    ca = subparsers.add_parser("assign-crew")
    ca.add_argument("--crew-id", type=int, required=True)
    ca.add_argument("--flight-id", type=int, required=True)
    ca.add_argument("--duty", required=True)
    ca.set_defaults(func=lambda args: print(
        "Crew assignment created with id",
        svc.assign_crew(args.crew_id, args.flight_id, args.duty)
    ))

    ca = subparsers.add_parser("list-assignments")
    ca.set_defaults(func=lambda args: pprint(svc.get_crew_assignments()))

    # =========================================================
    # USER
    # =========================================================
    u = subparsers.add_parser("add-user")
    u.add_argument("--username", required=True)
    u.add_argument("--password", required=True)
    u.add_argument("--role", choices=["admin", "staff", "customer"], required=True)
    u.set_defaults(func=lambda args: print(
        "User created with id",
        svc.add_user(args.username, args.password, args.role)
    ))

    u = subparsers.add_parser("list-users")
    u.set_defaults(func=lambda args: pprint(svc.get_users()))

    # =========================================================
    # UPDATE
    # =========================================================
    upd = subparsers.add_parser("update")
    upd.add_argument("--type", choices=[
        "passenger", "airport", "aircraft", "flight",
        "booking", "ticket", "crew", "assignment", "user"
    ], required=True)
    upd.add_argument("--id", type=int, required=True)
    upd.add_argument("--name")
    upd.add_argument("--email")
    upd.add_argument("--code")
    upd.add_argument("--city")
    upd.add_argument("--country")
    upd.add_argument("--model")
    upd.add_argument("--capacity", type=int)
    upd.add_argument("--departure-airport", type=int)
    upd.add_argument("--arrival-airport", type=int)
    upd.add_argument("--departure")
    upd.add_argument("--arrival")
    upd.add_argument("--aircraft-id", type=int)
    upd.add_argument("--price", type=float)
    upd.add_argument("--status")
    upd.add_argument("--seat-no")
    upd.add_argument("--ticket-no")
    upd.add_argument("--class", dest="ticket_class",
                     choices=["ECONOMY", "BUSINESS", "FIRST"])
    upd.add_argument("--role")
    upd.add_argument("--duty")
    upd.add_argument("--username")
    upd.add_argument("--password")
    upd.add_argument("--crew-id", type=int)
    upd.add_argument("--flight-id", type=int)

    def do_update(args):
        if args.type == "passenger":
            pprint(svc.update_passenger(args.id, args.name, args.email))
        elif args.type == "airport":
            pprint(svc.update_airport(args.id, args.code, args.name, args.city, args.country))
        elif args.type == "aircraft":
            pprint(svc.update_aircraft(args.id, args.model, args.capacity))
        elif args.type == "flight":
            pprint(svc.update_flight(args.id,
                                     code=args.code,
                                     departure_airport_id=args.departure_airport,
                                     arrival_airport_id=args.arrival_airport,
                                     departure_time=args.departure,
                                     arrival_time=args.arrival,
                                     aircraft_id=args.aircraft_id,
                                     base_price=args.price))
        elif args.type == "booking":
            pprint(svc.update_booking(args.id, args.status, args.price))
        elif args.type == "ticket":
            pprint(svc.dal.update_ticket(args.id, args.ticket_no, args.seat_no, args.ticket_class))
        elif args.type == "crew":
            pprint(svc.update_crew_member(args.id, args.name, args.role))
        elif args.type == "assignment":
            pprint(svc.update_crew_assignment(args.id,
                                              args.crew_id,
                                              args.flight_id,
                                              args.duty))
        elif args.type == "user":
            pprint(svc.update_user(args.id, args.username, args.password, args.role))
    upd.set_defaults(func=do_update)

    # =========================================================
    # DELETE
    # =========================================================
    d = subparsers.add_parser("delete")
    d.add_argument("--type", choices=[
        "passenger", "airport", "aircraft", "flight",
        "booking", "ticket", "crew", "assignment", "user"
    ], required=True)
    d.add_argument("--id", type=int, required=True)

    def do_delete(args):
        mapping = {
            "passenger": svc.delete_passenger,
            "airport": svc.delete_airport,
            "aircraft": svc.delete_aircraft,
            "flight": svc.delete_flight,
            "booking": svc.cancel_booking,
            "ticket": svc.dal.delete_ticket,
            "crew": svc.delete_crew_member,
            "assignment": svc.delete_crew_assignment,
            "user": svc.delete_user,
        }
        print("Deleted:", mapping[args.type](args.id))

    d.set_defaults(func=do_delete)

    # =========================================================
    # REPORTS (Advanced SQL)
    # =========================================================
    tp = subparsers.add_parser("top-passengers")
    tp.set_defaults(func=lambda args: pprint(svc.dal.top_passengers()))

    rr = subparsers.add_parser("revenue-rankings")
    rr.set_defaults(func=lambda args: pprint(svc.dal.revenue_rankings()))

    lf = subparsers.add_parser("route-load-factors")
    lf.set_defaults(func=lambda args: pprint(svc.dal.route_load_factors()))

    # =========================================================
    # Parse
    # =========================================================
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
