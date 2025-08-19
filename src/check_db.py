import sqlite3

def show_table(conn, table):
    print(f"\n--- {table.upper()} ---")
    try:
        cur = conn.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        if not rows:
            print("No data found.")
        else:
            col_names = [description[0] for description in cur.description]
            print(" | ".join(col_names))
            for row in rows:
                print(" | ".join(str(x) if x is not None else "" for x in row))
    except Exception as e:
        print(f"Error reading {table}: {e}")

def main():
    db_path = "airline.db"  # adjust if your DB is named differently
    conn = sqlite3.connect(db_path)

    # check which tables exist
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cur.fetchall()]
    print("Existing tables:", tables)

    # show contents of expected tables
    for table in ["passenger", "flight", "booking"]:
        if table in tables:
            show_table(conn, table)

    conn.close()

if __name__ == "__main__":
    main()
