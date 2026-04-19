import httpx
import os

MCP_BASE = os.getenv("MCP_SERVER_URL", "http://mcp-server:3000")


async def get_active_work_orders() -> list[dict]:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{MCP_BASE}/tools/get_active_work_orders",
            json={},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()
