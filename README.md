# Wi-Fi Assisted Smart Human Monitoring and Tracking System

A software-based monitoring dashboard designed to demonstrate device status monitoring, zone information, and recent activity history using a FastAPI backend and a web-based frontend.

> **Project status:** Prototype / Development  
> **Note:** The current version uses demo device data. Real-time college Wi-Fi device discovery and precise indoor positioning are not yet integrated.

## 1. Project Overview

The Wi-Fi Assisted Smart Human Monitoring and Tracking System is a software prototype that demonstrates how connected-device information could be organized and monitored through a centralized dashboard.

The system provides a web interface to view device information, update connection status, and review recent activity events.

The project is being developed as a software-only final-year engineering project, with future scope for authorized network integration and indoor location estimation.

## 2. Objectives

- Develop a web-based device monitoring dashboard.
- Display device information and connection status.
- Support Connect and Disconnect actions in the prototype.
- Display recent device activity and event history.
- Use a Python FastAPI backend to handle API requests.
- Explore database-backed activity logging.
- Prepare the system for future integration with authorized Wi-Fi infrastructure.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| Uvicorn | Running the FastAPI application |
| HTML | Dashboard structure |
| CSS | Dashboard styling |
| JavaScript | Frontend interactions and API communication |
| SQLite | Local database technology used or explored by the project |
| Git and GitHub | Version control and source code hosting |
| Visual Studio Code | Development environment |

## 4. Project Structure

```text
WiFiHumanMonitoring/
│
├── backend/
│   └── main.py
│       # FastAPI application and backend API logic
│
├── frontend/
│   ├── index.html
│   │   # Dashboard UI, styling and browser-side interactions
│   │
│   └── index_backup.html
│       # Local backup of the previous dashboard
│
├── check_db.py
│   # Database inspection / verification script
│
├── .venv/
│   # Local Python virtual environment
│
├── .gitignore
│   # Git exclusion rules, if configured
│
├── requirements.txt
│   # Python dependencies, if present
│
└── README.md
    # Project documentation
```

**Note:** The structure above lists the files identified during development. Confirm the actual presence of `.gitignore`, `requirements.txt`, and any database files in VS Code before treating them as existing project files. The backup file is for local recovery and does not need to be committed to GitHub.

## 5. System Architecture

```text
User
  |
  v
Web Dashboard
(frontend/index.html)
  |
  | HTTP requests
  v
FastAPI Backend
(backend/main.py)
  |
  v
Device Data and Activity History
  |
  v
Dashboard Updates
```

The frontend sends API requests to the backend. The backend processes the request and returns device information or activity data. The frontend then updates the dashboard.

The architecture can later be extended to receive data from authorized campus network infrastructure.

## 6. Current Features

### Device Monitoring Dashboard

- Displays device information.
- Shows connection status.
- Provides a dashboard interface for monitoring the prototype's device records.

### Connect and Disconnect

- Allows the user to change a device's status through the dashboard.
- Sends the status update to the backend.
- Displays the updated status when the request succeeds.

### Recent Device Activity

- Displays recent device events.
- Shows available device identifiers, events, zones, and timestamps.
- Refreshes activity information from the backend.

### Backend API

- Handles frontend requests.
- Provides device information and status updates.
- Supports activity-history retrieval.

## 7. Development Setup

### Prerequisites

- Python installed on Windows.
- Visual Studio Code.
- Git installed.
- A web browser.
- The project repository cloned or downloaded locally.

### Step 1: Open the project

Open the `WiFiHumanMonitoring` folder in Visual Studio Code.

### Step 2: Activate the virtual environment

In the VS Code PowerShell terminal, run:

```powershell
.\.venv\Scripts\Activate.ps1
```

If the virtual environment is already activated, continue to the next step.

### Step 3: Install dependencies

If a `requirements.txt` file exists, run:

```powershell
python -m pip install -r requirements.txt
```

If the file does not exist, create it from the project's actual Python dependencies before using this command.

### Step 4: Start the backend

From the project root directory, run:

```powershell
python -m uvicorn backend.main:app --reload
```

The development server should be available at:

`http://127.0.0.1:8000`

### Step 5: Verify the backend

Open these endpoints in a browser:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/api/devices`

The available responses depend on the implementation in `backend/main.py`.

FastAPI's interactive API documentation is normally available at:

`http://127.0.0.1:8000/docs`

### Step 6: Open the frontend

Open `frontend/index.html` using the Live Server extension in VS Code if that is how the current project is configured.

The frontend must use the correct backend API address. Keep the backend running while testing dashboard actions.

## 8. API Endpoints

The following routes have been used during project development.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Backend root endpoint |
| GET | `/health` | Health check |
| GET | `/api/devices` | Retrieve device records |
| GET | `/api/devices/{device_id}` | Retrieve a specific device |
| PATCH | `/api/devices/{device_id}` | Update a device's status or supported fields |
| GET | `/api/history?limit=50` | Retrieve recent activity history |

The precise request fields, validation rules, response format, and persistence behavior should be verified against the current backend implementation.

## 9. Testing Checklist

- [ ] Start the FastAPI backend successfully.
- [ ] Verify that the dashboard loads.
- [ ] Confirm that device information is displayed.
- [ ] Test the Connect action.
- [ ] Test the Disconnect action.
- [ ] Verify that the status changes are reflected on the dashboard.
- [ ] Check the Recent Device Activity section.
- [ ] Verify API responses through `/docs`.
- [ ] Check whether activity records persist after restarting the backend.
- [ ] Test the dashboard after refreshing the browser.

## 10. Current Limitations

- Device records currently represent prototype/demo data.
- The dashboard does not independently discover every device connected to the college Wi-Fi network.
- A displayed zone does not establish a device's exact physical indoor position.
- Real-world monitoring requires authorized access to network telemetry or controller APIs.
- Indoor positioning accuracy depends on available infrastructure, measurement methods, and validation.
- Database persistence must be verified separately; displaying history in the UI alone does not guarantee permanent storage.

## 11. Future Enhancements

- Integrate with authorized campus Wi-Fi infrastructure.
- Retrieve live device connection events where permitted.
- Improve device inventory and zone visualization.
- Validate database-backed activity persistence.
- Add authentication and role-based access control.
- Add monitoring logs, error handling, and API tests.
- Improve responsive design for mobile and desktop.
- Evaluate privacy-preserving indoor location estimation methods.
- Add clear data-retention and access policies.

## 12. Privacy and Security

This project should be developed and tested only with authorized devices and network infrastructure.

Before integrating with a real college network, obtain the required approval from the institution's IT team. Limit access to device identifiers and activity records, avoid collecting unnecessary personal information, and protect any credentials or API keys.

Do not commit secrets, local environment files, or sensitive network information to GitHub.

## 13. Version Control

The project uses Git for version control and GitHub for source code hosting.

Example commands for committing future changes:

```powershell
git status
git add backend/main.py frontend/index.html README.md
git commit -m "Update monitoring dashboard documentation"
git push origin main
```

Review staged files before committing so that backup files, generated data, credentials, and unrelated files are not accidentally uploaded.

## 14. Conclusion

The current prototype establishes a foundation for a Wi-Fi-assisted monitoring dashboard with a FastAPI backend, device status updates, and recent activity visualization.

Future development will focus on reliable data persistence, improved dashboard design, and authorized campus network integration. Any real-world tracking capability must be implemented and validated separately from the current demo.

---

**Repository:** [wifi-human-monitoring-system](https://github.com/Sankar2316/wifi-human-monitoring-system)
