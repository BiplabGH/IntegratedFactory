import random
from .base_machine import BaseMachine


class CNCMachine(BaseMachine):
    def machine_type(self) -> str:
        return "cnc"

    def generate_telemetry(self) -> dict:
        return {
            "spindle_speed_rpm": round(random.gauss(3000, 50), 1),
            "feed_rate_mm_min": round(random.gauss(500, 10), 1),
            "tool_wear_percent": round(random.uniform(0, 100), 2),
            "coolant_temp_c": round(random.gauss(25, 2), 2),
            "vibration_mm_s": round(abs(random.gauss(0.5, 0.1)), 3),
            "parts_produced": random.randint(0, 5),
        }
