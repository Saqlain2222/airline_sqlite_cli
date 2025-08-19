import sqlite3

def list_columns(db_path="airline.db"):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        # fetch all tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cur.fetchall()]

        print("=== Column Names in Each Table ===")
        for table in tables:
            cur.execute(f"PRAGMA table_info({table});")
            cols = cur.fetchall()
            col_names = [c[1] for c in cols]
            print(f"\nTable: {table}")
            print("Columns:", ", ".join(col_names))

if __name__ == "__main__":
    list_columns()
