# Homelab Dashboard (FastAPI + SQLite)

Simple, self-hosted dashboard for your homelab services.

## What you get

- Add, edit, and delete service links
- Card-based dashboard layout
- Optional service status checks (online/offline)
- Quick notes panel
- Mobile-friendly web UI
- SQLite database persisted on `/data`
- Docker Compose startup with healthcheck

## Requirements

- Docker and Docker Compose installed
- Raspberry Pi 4 (ARM64) or x86 machine

## Quick Start (non-developer friendly)

1. Copy project files to your machine.
2. Open terminal in this folder.
3. Create env file:

```bash
cp .env.example .env
```

Windows PowerShell alternative:

```powershell
Copy-Item .env.example .env
```

4. Start the app:

```bash
docker-compose up -d
```

5. Open your browser:

- `http://<your-server-ip>:<APP_PORT>`
- Example with defaults: `http://localhost:8000`

## Data persistence

- Database file is stored in bind-mounted folder: `./data` on host mapped to `/data` in container.
- Restarting container keeps your services/notes data.

## Basic commands

Start:

```bash
docker-compose up -d
```

Stop:

```bash
docker-compose down
```

View logs:

```bash
docker-compose logs -f
```

Rebuild after changes:

```bash
docker-compose up -d --build
```

## Environment variables (.env)

- `APP_HOST` default `0.0.0.0`
- `APP_PORT` default `8000` (used by both container app port and published host port)
- `DATABASE_PATH` default `/data/dashboard.db`
- `APP_NAME` dashboard title
- `DATA_DIR` host data directory bind mount (defaults to `./data`)

Example `.env`:

```env
APP_HOST=0.0.0.0
APP_PORT=8000
DATABASE_PATH=/data/dashboard.db
APP_NAME=Homelab Dashboard
DATA_DIR=./data
```

## Healthcheck

Container health endpoint:

- `GET /health`

Docker healthcheck verifies this endpoint every 30 seconds.

## Run tests

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
pytest
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
```

## Project structure

```text
.
├── app
│   ├── main.py
│   ├── db.py
│   ├── status.py
│   ├── static
│   │   ├── app.js
│   │   └── style.css
│   └── templates
│       ├── base.html
│       └── dashboard.html
├── tests
│   └── test_app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Notes for Raspberry Pi 4 (ARM64)

- `python:3.12-slim` base image is multi-arch and supports ARM64 and x86.
- Dependencies are architecture-neutral or broadly available on ARM64.
- No architecture-specific app code is used.

## Done checklist

- [x] Build succeeds
- [x] Runs with Docker Compose
- [x] ARM64/x86 compatible image base
- [x] SQLite persisted in bind mount
- [x] Healthcheck included
- [x] Basic tests included
