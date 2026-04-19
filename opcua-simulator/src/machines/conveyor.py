import random
from .base_machine import BaseMachine


class ConveyorBelt(BaseMachine):
    def machine_type(self) -> str:
        return "conveyor"

    def generate_telemetry(self) -> dict:
        return {
            "belt_speed_m_min": round(random.gauss(10, 0.5), 2),
            "load_kg": round(random.uniform(0, 500), 1),
            "motor_temp_c": round(random.gauss(45, 3), 2),
            "items_on_belt": random.randint(0, 20),
        }
