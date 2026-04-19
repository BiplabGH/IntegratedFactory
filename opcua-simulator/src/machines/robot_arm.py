import random
from .base_machine import BaseMachine


class RobotArm(BaseMachine):
    def machine_type(self) -> str:
        return "robot_arm"

    def generate_telemetry(self) -> dict:
        return {
            "joint_angles_deg": [round(random.gauss(0, 30), 2) for _ in range(6)],
            "payload_kg": round(random.uniform(0, 10), 2),
            "cycle_time_s": round(random.gauss(5, 0.3), 3),
            "position": {
                "x": round(random.gauss(0, 100), 2),
                "y": round(random.gauss(0, 100), 2),
                "z": round(random.gauss(500, 50), 2),
            },
            "gripper_force_n": round(random.uniform(0, 100), 1),
        }
