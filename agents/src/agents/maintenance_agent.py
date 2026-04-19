import asyncio
import json
import logging
import anthropic
from ..tools.historian_tool import get_metric_history

logger = logging.getLogger("maintenance-agent")

TOOLS = [
    {
        "name": "get_metric_history",
        "description": "Fetch hourly aggregated metric history for predictive analysis",
        "input_schema": {
            "type": "object",
            "properties": {
                "machine_id": {"type": "string"},
                "metric_name": {"type": "string"},
                "hours": {"type": "integer", "default": 24},
            },
            "required": ["machine_id", "metric_name"],
        },
    }
]


class MaintenanceAgent:
    def __init__(self, machine_ids: list[str], model: str = "claude-sonnet-4-6"):
        self.machine_ids = machine_ids
        self.model = model
        self.client = anthropic.AsyncAnthropic()

    async def predict_maintenance(self, machine_id: str) -> str:
        messages = [
            {
                "role": "user",
                "content": (
                    f"Predict maintenance needs for machine {machine_id} based on the last 24 hours. "
                    "Check tool_wear_percent and motor_temp_c trends. "
                    "Use get_metric_history for each metric, then predict when maintenance is due."
                ),
            }
        ]

        while True:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                tools=TOOLS,
                messages=messages,
            )

            if response.stop_reason == "tool_use":
                tool_use = next(b for b in response.content if b.type == "tool_use")
                result = await get_metric_history(**tool_use.input)
                messages += [
                    {"role": "assistant", "content": response.content},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use.id,
                                "content": json.dumps(result),
                            }
                        ],
                    },
                ]
            else:
                text = next((b.text for b in response.content if hasattr(b, "text")), "")
                return text

    async def run_loop(self, interval_seconds: int = 300):
        logger.info("MaintenanceAgent started")
        while True:
            for machine_id in self.machine_ids:
                try:
                    prediction = await self.predict_maintenance(machine_id)
                    logger.info("[%s] Maintenance: %s", machine_id, prediction)
                except Exception as e:
                    logger.error("[%s] Error: %s", machine_id, e)
            await asyncio.sleep(interval_seconds)
