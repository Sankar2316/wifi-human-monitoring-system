
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "monitoring.db"

app = FastAPI(
    title="Wi-Fi Human Monitoring System",
    description="Device monitoring API with SQLite history",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def current_time():
    return datetime.now(timezone.utc).isoformat()


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY,
                device_type TEXT NOT NULL,
                status TEXT NOT NULL,
                zone TEXT NOT NULL,
                last_seen TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS device_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                zone TEXT NOT NULL,
                event_time TEXT NOT NULL
            )
        """)

        demo_devices = [
            (
                "DEV-001",
                "Mobile",
                "Connected",
                "ECE Block - Demo Zone A",
                current_time(),
            ),
            (
                "DEV-002",
                "Laptop",
                "Connected",
                "ECE Block - Demo Zone B",
                current_time(),
            ),
            (
                "DEV-003",
                "Tablet",
                "Disconnected",
                "Unknown",
                current_time(),
            ),
        ]

        connection.executemany("""
            INSERT OR IGNORE INTO devices
            (device_id, device_type, status, zone, last_seen)
            VALUES (?, ?, ?, ?, ?)
        """, demo_devices)

        existing_history = connection.execute(
            "SELECT COUNT(*) FROM device_history"
        ).fetchone()[0]

        if existing_history == 0:
            for device in demo_devices:
                connection.execute("""
                    INSERT INTO device_history
                    (device_id, event_type, zone, event_time)
                    VALUES (?, ?, ?, ?)
                """, (
                    device[0],
                    "DEMO_INITIAL_RECORD",
                    device[3],
                    device[4],
                ))


init_db()


@app.get("/")
def home():
    return {
        "message": "Wi-Fi Human Monitoring API is running!",
        "status": "success",
        "database": "SQLite",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    with get_connection() as connection:
        connection.execute("SELECT 1").fetchone()

    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": current_time(),
    }


@app.get("/api/devices")
def get_devices():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT device_id, device_type, status, zone, last_seen
            FROM devices
            ORDER BY device_id
        """).fetchall()

    devices = [dict(row) for row in rows]

    return {
        "count": len(devices),
        "devices": devices,
        "data_source": "DEMO - SQLite database, not real Wi-Fi data",
    }


@app.get("/api/devices/{device_id}")
def get_device(device_id: str):
    with get_connection() as connection:
        row = connection.execute("""
            SELECT device_id, device_type, status, zone, last_seen
            FROM devices
            WHERE device_id = ?
        """, (device_id,)).fetchone()

    if row is None:
        return {
            "error": "Device not found",
            "device_id": device_id,
        }

    return dict(row)


@app.get("/api/history")
def get_history(limit: int = 50):
    # Keep requests bounded to avoid returning excessive records.
    limit = max(1, min(limit, 200))

    with get_connection() as connection:
        rows = connection.execute("""
            SELECT id, device_id, event_type, zone, event_time
            FROM device_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

    return {
        "count": len(rows),
        "history": [dict(row) for row in rows],
        "note": "Initial entries are demo records, not live tracking events.",
    }

from pydantic import BaseModel

class DeviceUpdate(BaseModel):
    status: str
    zone: str

@app.patch("/api/devices/{device_id}")
def update_device(device_id: str, update: DeviceUpdate):
    allowed_statuses = {"Connected", "Disconnected"}

    if update.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Status must be Connected or Disconnected"
        )

    conn = get_connection()

    try:
        device = conn.execute(
            "SELECT * FROM devices WHERE device_id = ?",
            (device_id,)
        ).fetchone()

        if device is None:
            raise HTTPException(
                status_code=404,
                detail="Device not found"
            )

        old_status = device["status"]
        old_zone = device["zone"]

        conn.execute(
            """
            UPDATE devices
            SET status = ?, zone = ?, last_seen = ?
            WHERE device_id = ?
            """,
            (
                update.status,
                update.zone,
                datetime.now(timezone.utc).isoformat(),
                device_id
            )
        )

        if old_status != update.status or old_zone != update.zone:
            conn.execute(
                """
                INSERT INTO device_history
                (device_id, event_type, zone, event_time)
                VALUES (?, ?, ?, ?)
                """,
                (
                    device_id,
                    f"STATUS_CHANGE: {old_status} -> {update.status}",
                    update.zone,
                    datetime.now(timezone.utc).isoformat()
                )
            )

        conn.commit()

        return {
            "message": "Device updated successfully",
            "device_id": device_id,
            "old_status": old_status,
            "new_status": update.status,
            "zone": update.zone
        }

    finally:
        conn.close()
