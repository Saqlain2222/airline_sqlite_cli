from src.services import Services

def run_tests():
    print("=== Security & Constraint Tests ===\n")

    # -------------------------
    # Role-Based Access Control
    # -------------------------
    print("1. RBAC Tests")

    try:
        print("CUSTOMER trying to add a flight (should fail)...")
        svc_customer = Services(current_user_role="CUSTOMER")
        svc_customer.add_flight(
            "TST100", 1, 2,
            "2025-11-01T10:00:00", "2025-11-01T12:00:00",
            1, 200.0
        )
    except PermissionError as e:
        print("Blocked:", e)

    try:
        print("\nSTAFF adding a flight (should succeed)...")
        svc_staff = Services(current_user_role="STAFF")
        flight_id = svc_staff.add_flight(
            "TST200", 1, 3,
            "2025-11-05T15:00:00", "2025-11-05T18:00:00",
            2, 350.0
        )
        print("Flight created with id:", flight_id)
    except Exception as e:
        print("Unexpected error:", e)

    try:
        print("\nADMIN adding a user (should succeed)...")
        svc_admin = Services(current_user_role="ADMIN")
        user_id = svc_admin.add_user("test_admin", "securepass", "ADMIN")
        print("User created with id:", user_id)
    except Exception as e:
        print("Unexpected error:", e)

    # -------------------------
    # Constraint Enforcement
    # -------------------------
    print("\n2. Constraint Tests")

    try:
        print("Adding flight with negative price (should fail)...")
        svc_staff = Services(current_user_role="STAFF")
        svc_staff.add_flight(
            "TST300", 1, 2,
            "2025-11-10T09:00:00", "2025-11-10T11:00:00",
            1, -50.0
        )
    except Exception as e:
        print("Blocked:", e)

    try:
        print("\nAdding duplicate ticket number (should fail)...")
        svc_admin = Services(current_user_role="ADMIN")

        # First booking
        booking_id = svc_admin.book(1, 1, "ECONOMY", 150.0, seat_no="22A")
        svc_admin.dal.create_ticket(booking_id, "DUPLICATE001", "22A", "ECONOMY")

        # Second insert with same ticket_no should fail
        svc_admin.dal.create_ticket(booking_id, "DUPLICATE001", "22B", "BUSINESS")
    except Exception as e:
        print("Blocked:", e)

    try:
        print("\nAdding duplicate booking (same passenger + flight, should fail)...")
        svc_admin = Services(current_user_role="ADMIN")
        svc_admin.book(1, 2, "ECONOMY", 100.0, seat_no="20A")  # First booking ok
        svc_admin.book(1, 2, "ECONOMY", 100.0, seat_no="20B")  # Duplicate
    except Exception as e:
        print("Blocked:", e)


if __name__ == "__main__":
    run_tests()
