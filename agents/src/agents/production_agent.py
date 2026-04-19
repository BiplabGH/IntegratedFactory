import asyncio
import json
import logging
import anthropic
from ..tools.mes_tool import get_active_work_orders
from ..tools.historian_tool import get_machine_metrics

logger = logging.getLogger("production-agent")

TOOLS = [
    {
        "name": "get_active_work_orders",
        "description": "List active work orders from Odoo MES",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_machine_metrics",
        "description": "Get recent machine telemetry",
        "input_schema": {
            "type": "object",
            "properties": {
                "machine_id": {"type": "string"},
                "minutes": {"type": "integer", "default": 15},
            },
            "required": ["machine_id"],
        },
    },
]

TOOL_DISPATCH = {
    "get_active_work_orders": lambda inp: get_active_work_orders(),
    "get_machine_metrics": lambda inp: get_machine_metrics(**inp),
}


class ProductionAgent:
    def __init__(self, model: str = "claude-sonnet-4-6"):
        self.model = model
        self.client = anthropic.AsyncAnthropic()

    async def assess_production(self) -> str:
        messages = [
            {
                "role": "user",
                "content": (
                    "Assess current production status. "
                    "Get active work orders from MES, then check machine metrics for any "
                    "machine assigned to those orders. Summarise production health."
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
                result = await TOOL_DISPATCH[tool_use.name](tool_use.input)
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

    async def run_loop(self, interval_seconds: int = 60):
        logger.info("ProductionAgent started")
        while True:
            try:
                summary = await self.assess_production()
                logger.info("Production summary: %s", summary)
            except Exception as e:
                logger.error("Production agent error: %s", e)
            await asyncio.sleep(interval_seconds)
