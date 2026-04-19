import asyncio
import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MachineStatus:
    machine_id: str
    machine_type: str
    timestamp: float = field(default_factory=time.time)
    running: bool = True
    error_code: int = 0
    telemetry: dict[str, Any] = field(default_factory=dict)


class BaseMachine(ABC):
    def __init__(self, machine_id: str, name: str, mqtt_topic: str, update_interval_ms: int):
        self.machine_id = machine_id
        self.name = name
        self.mqtt_topic = mqtt_topic
        self.update_interval_s = update_interval_ms / 1000.0
        self._running = False

    @abstractmethod
    def generate_telemetry(self) -> dict[str, Any]:
        """Return current telemetry snapshot."""

    @abstractmethod
    def machine_type(self) -> str:
        ...

    def to_payload(self) -> str:
        status = MachineStatus(
            machine_id=self.machine_id,
            machine_type=self.machine_type(),
            telemetry=self.generate_telemetry(),
        )
        return json.dumps(
            {
                "machine_id": status.machine_id,
                "machine_type": status.machine_type,
                "timestamp": status.timestamp,
                "running": status.running,
                "error_code": status.error_code,
                "telemetry": status.telemetry,
            }
        )

    async def run(self, on_update):
        self._running = True
        while self._running:
            payload = self.to_payload()
            await on_update(self.mqtt_topic, payload)
            await asyncio.sleep(self.update_interval_s)

    def stop(self):
        self._running = False
