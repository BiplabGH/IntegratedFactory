import asyncio
import json
import logging
import os
import anthropic
from ..tools.historian_tool import get_machine_metrics

logger = logging.getLogger("quality-agent")

TOOL_WEAR_THRESHOLD = float(os.getenv("TOOL_WEAR_THRESHOLD", "80"))
VIBRATION_THRESHOLD = float(os.getenv("VIBRATION_THRESHOLD", "1.0"))

TOOLS = [
    {
        "name": "get_machine_metrics",
        "description": "Fetch recent telemetry for a machine from the historian",
        "input_schema": {
            "type": "object",
            "properties": {
                "machine_id": {"type": "string"},
                "minutes": {"type": "integer", "default": 30},
            },
            "required": ["machine_id"],
        },
    }
]


class QualityAgent:
    def __init__(self, machine_ids: list[str], model: str = "claude-sonnet-4-6"):
        self.machine_ids = machine_ids
        self.model = model
        self.client = anthropic.AsyncAnthropic()

    async def analyse(self, machine_id: str) -> str:
        messages = [
            {
                "role": "user",
                "content": (
                    f"Analyse quality metrics for machine {machine_id}. "
                    f"Flag if tool_wear_percent > {TOOL_WEAR_THRESHOLD}% or "
                    f"vibration_mm_s > {VIBRATION_THRESHOLD}. "
                    "Use the get_machine_metrics tool, then provide a brief quality assessment."
                ),
            }
        ]

        while True:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=512,
                tools=TOOLS,
                messages=messages,
            )

            if response.stop_reason == "tool_use":
                tool_use = next(b for b in response.content if b.type == "tool_use")
                result = await get_machine_metrics(**tool_use.input)
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

    async def run_loop(self, interval_seconds: int = 30):
        logger.info("QualityAgent started for machines: %s", self.machine_ids)
        while True:
            for machine_id in self.machine_ids:
                try:
                    assessment = await self.analyse(machine_id)
                    logger.info("[%s] Quality: %s", machine_id, assessment)
                except Exception as e:
                    logger.error("[%s] Error: %s", machine_id, e)
            await asyncio.sleep(interval_seconds)
