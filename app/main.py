import os
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .db import (
    create_service,
    delete_service,
    get_notes,
    init_db,
    list_services,
    update_notes,
    update_service,
)
from .status import check_service

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title=os.getenv("APP_NAME", "Homelab Dashboard"))
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/")
def dashboard(request: Request):
    services = list_services()
    notes = get_notes()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "app_name": os.getenv("APP_NAME", "Homelab Dashboard"),
            "services": services,
            "notes": notes,
        },
    )


@app.post("/services")
def add_service(
    name: str = Form(...),
    url: str = Form(...),
    description: str = Form(""),
    status_enabled: str | None = Form(None),
):
    create_service(name, url, description, status_enabled == "on")
    return RedirectResponse(url="/", status_code=303)


@app.post("/services/{service_id}/edit")
def edit_service(
    service_id: int,
    name: str = Form(...),
    url: str = Form(...),
    description: str = Form(""),
    status_enabled: str | None = Form(None),
):
    update_service(service_id, name, url, description, status_enabled == "on")
    return RedirectResponse(url="/", status_code=303)


@app.post("/services/{service_id}/delete")
def remove_service(service_id: int):
    delete_service(service_id)
    return RedirectResponse(url="/", status_code=303)


@app.post("/notes")
def save_notes(content: str = Form("")):
    update_notes(content)
    return RedirectResponse(url="/", status_code=303)


@app.get("/api/statuses")
async def service_statuses() -> dict:
    services = list_services()
    results = {}
    for service in services:
        if service["status_enabled"]:
            results[service["id"]] = await check_service(service["url"])
        else:
            results[service["id"]] = {"status": "disabled", "status_code": None}
    return {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "services": results,
    }
