# main.py
from src import db

if __name__ == "__main__":
    db.apply_schema()
    db.seed_demo()
    print("Database initialized and demo data inserted.")
