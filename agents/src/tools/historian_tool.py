import httpx
import os

MCP_BASE = os.getenv("MCP_SERVER_URL", "http://mcp-server:3000")


async def get_machine_metrics(machine_id: str, minutes: int = 60) -> list[dict]:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{MCP_BASE}/tools/get_raw_historian",
            json={"machine_id": machine_id, "minutes": minutes},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()


async def get_metric_history(machine_id: str, metric_name: str, hours: int = 1) -> list[dict]:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{MCP_BASE}/tools/get_machine_metric_history",
            json={"machine_id": machine_id, "metric_name": metric_name, "hours": hours},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()
