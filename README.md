
# Process Monitor (Django + Agent)

A minimal, production-ready starter for a Windows Process Monitoring system.

## What you get

- Django + DRF backend (SQLite)
- API-key auth for the agent
- Endpoints to ingest and read latest/historical data
- Static frontend (no build tools) with a multi-computer sidebar and expandable process tree
- Python agent (can be compiled to a single EXE with PyInstaller)

---

## Quickstart

```bash
# 1) Setup a venv and install deps
python -m venv .venv
. .venv/Scripts/activate  # on Windows
# or: source .venv/bin/activate (Linux/Mac)
pip install -r requirements.txt

# 2) Migrate and run
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Open http://localhost:8000 in your browser.

### Configure API keys

In `process_monitor/settings.py` set:
```python
AGENT_API_KEYS = ["changeme123"]
```
Use the same key in the agent `agent/config.ini` or env var.

---

## API Overview

- `POST /api/ingest/` (Agent)
  - Headers: `Authorization: Api-Key <YOUR_KEY>`
  - JSON:
    ```json
    {
      "hostname": "COMPUTER_1",
      "system": { "os": "...", "cpu_model": "...", "cores": 8, "threads": 16, "ram_total_gb": 16, "ram_used_gb": 8, "ram_available_gb": 8, "storage_total_gb": 195, "storage_used_gb": 183, "storage_free_gb": 12 },
      "processes": [ { "pid": 1, "ppid": 0, "name": "System", "cpu": 0.1, "mem_mb": 12.3 } ]
    }
    ```

- `GET /api/computers/` → list computers

- `GET /api/computers/<hostname>/latest/` → latest snapshot + processes

- `GET /api/snapshots/<hostname>/` → historical snapshots (ids, timestamps)

- `GET /api/snapshots/<id>/` → snapshot details

---

## Agent

Edit `agent/config.ini`, then run `agent/agent.py`. To build a single-file EXE:

```bash
pip install pyinstaller
pyinstaller --onefile --name process-agent agent/agent.py
```

Double-click the EXE to send one snapshot. To run periodically, use Windows Task Scheduler.

---

## Frontend

A single `index.html` in `frontend/` (served by Django) shows:
- Computers in a sidebar
- Click to switch machines
- Expandable process hierarchy
- Refresh button and auto-refresh toggle
- Hostname + system card like your screenshot

No build step required.
