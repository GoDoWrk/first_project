from typing import Any

import httpx


async def check_service(url: str, timeout_seconds: float = 4.0) -> dict[str, Any]:
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=timeout_seconds) as client:
            response = await client.get(url)
        return {
            "status": "online" if response.status_code < 500 else "offline",
            "status_code": response.status_code,
        }
    except Exception:
        return {"status": "offline", "status_code": None}
