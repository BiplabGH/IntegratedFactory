import time
from collections import defaultdict
from typing import Any


class Aggregator:
    def __init__(self, window_seconds: int = 60):
        self.window_seconds = window_seconds
        self._buckets: dict[str, list] = defaultdict(list)
        self._last_flush: dict[str, float] = {}

    def process(self, data: dict[str, Any]) -> dict | None:
        machine_id = data.get("machine_id", "unknown")
        self._buckets[machine_id].append(data)

        now = time.time()
        last = self._last_flush.get(machine_id, 0)

        if now - last >= self.window_seconds:
            result = self._flush(machine_id, now)
            self._last_flush[machine_id] = now
            return result
        return None

    def _flush(self, machine_id: str, ts: float) -> dict:
        records = self._buckets.pop(machine_id, [])
        if not records:
            return {}

        telemetry_keys = set()
        for r in records:
            telemetry_keys.update(r.get("telemetry", {}).keys())

        aggregated_telemetry = {}
        for key in telemetry_keys:
            values = [
                r["telemetry"][key]
                for r in records
                if isinstance(r.get("telemetry", {}).get(key), (int, float))
            ]
            if values:
                aggregated_telemetry[key] = {
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "count": len(values),
                }

        return {
            "machine_id": machine_id,
            "window_start": ts - self.window_seconds,
            "window_end": ts,
            "sample_count": len(records),
            "telemetry": aggregated_telemetry,
        }
