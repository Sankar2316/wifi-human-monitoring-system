
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "monitoring.db"

print("Database path:", DB_PATH)
print("Database exists:", DB_PATH.exists())

if DB_PATH.exists():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for table in ["devices", "device_history"]:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table,)
        )
        exists = cursor.fetchone()

        if exists:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            print(f"{table} records:", cursor.fetchone()[0])

            cursor.execute(f"SELECT * FROM {table} LIMIT 5")
            print(f"{table} sample:", cursor.fetchall())
        else:
            print(f"Table missing: {table}")

    conn.close()
