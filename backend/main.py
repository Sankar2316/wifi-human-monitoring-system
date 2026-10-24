
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Wi-Fi Human Monitoring System",
    description="Backend API for authorized Wi-Fi device monitoring",
    version="1.0.0",
)

# Allow our frontend to connect during local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data for development only.
# These are NOT real college Wi-Fi devices.
devices = [
    {
        "device_id": "DEV-001",
        "device_type": "Mobile",
        "status": "Connected",
        "zone": "ECE Block - Demo Zone A",
        "last_seen": datetime.now(timezone.utc).isoformat(),
    },
    {
        "device_id": "DEV-002",
        "device_type": "Laptop",
        "status": "Connected",
        "zone": "ECE Block - Demo Zone B",
        "last_seen": datetime.now(timezone.utc).isoformat(),
    },
    {
        "device_id": "DEV-003",
        "device_type": "Tablet",
        "status": "Disconnected",
        "zone": "Unknown",
        "last_seen": datetime.now(timezone.utc).isoformat(),
    },
]


@app.get("/")
def home():
    return {
        "message": "Wi-Fi Human Monitoring API is running!",
        "status": "success",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/devices")
def get_devices():
    return {
        "count": len(devices),
        "devices": devices,
        "data_source": "DEMO - not real Wi-Fi data",
    }


@app.get("/api/devices/{device_id}")
def get_device(device_id: str):
    for device in devices:
        if device["device_id"] == device_id:
            return device

    return {
        "error": "Device not found",
        "device_id": device_id,
    }
