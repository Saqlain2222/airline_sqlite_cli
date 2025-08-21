PRAGMA foreign_keys = ON;

-- ==========================
-- Lookup tables
-- ==========================
CREATE TABLE IF NOT EXISTS airport (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  code    TEXT NOT NULL UNIQUE CHECK (length(code)=3), -- enforce IATA 3-char code
  name    TEXT NOT NULL,
  city    TEXT NOT NULL,
  country TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS aircraft (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  model    TEXT NOT NULL,
  capacity INTEGER NOT NULL CHECK (capacity > 0),
  UNIQUE(model, capacity) -- prevent duplicates
);

-- ==========================
-- Core entities
-- ==========================
CREATE TABLE IF NOT EXISTS passenger (
  id    INTEGER PRIMARY KEY AUTOINCREMENT,
  name  TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS flight (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  code         TEXT NOT NULL UNIQUE,
  departure_airport_id INTEGER NOT NULL REFERENCES airport(id) ON DELETE RESTRICT,
  arrival_airport_id   INTEGER NOT NULL REFERENCES airport(id) ON DELETE RESTRICT,
  departure_time TEXT NOT NULL, -- ISO 8601 string
  arrival_time   TEXT NOT NULL,
  aircraft_id    INTEGER NOT NULL REFERENCES aircraft(id) ON DELETE RESTRICT,
  base_price     REAL NOT NULL CHECK (base_price >= 0)
);

CREATE TABLE IF NOT EXISTS booking (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  passenger_id INTEGER NOT NULL REFERENCES passenger(id) ON DELETE RESTRICT,
  flight_id    INTEGER NOT NULL REFERENCES flight(id) ON DELETE RESTRICT,
  status       TEXT NOT NULL CHECK (status IN ('BOOKED','CANCELLED')),
  booked_at    TEXT NOT NULL DEFAULT (datetime('now')),
  price        REAL NOT NULL CHECK (price >= 0),
  UNIQUE(passenger_id, flight_id) -- no duplicate bookings per passenger
);

CREATE TABLE IF NOT EXISTS ticket (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  booking_id INTEGER NOT NULL REFERENCES booking(id) ON DELETE CASCADE,
  ticket_no  TEXT NOT NULL UNIQUE,
  seat_no    TEXT NOT NULL,
  class      TEXT NOT NULL CHECK (class IN ('ECONOMY','BUSINESS','FIRST'))
);

CREATE TABLE IF NOT EXISTS crew_member (
  id   INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crew_assignment (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  crew_member_id INTEGER NOT NULL REFERENCES crew_member(id) ON DELETE RESTRICT,
  flight_id      INTEGER NOT NULL REFERENCES flight(id) ON DELETE RESTRICT,
  duty           TEXT NOT NULL,
  UNIQUE(crew_member_id, flight_id) -- avoid duplicate assignment
);

-- ==========================
-- Simple RBAC (authentication/authorisation)
-- ==========================
CREATE TABLE IF NOT EXISTS user (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  username      TEXT NOT NULL UNIQUE,
  password_hash BLOB NOT NULL,
  salt          BLOB NOT NULL,
  role          TEXT NOT NULL CHECK (role IN ('ADMIN','STAFF','CUSTOMER'))
);

-- ==========================
-- Indexes (performance)
-- ==========================
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
