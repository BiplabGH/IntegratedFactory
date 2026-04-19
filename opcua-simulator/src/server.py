import asyncio
import os
import yaml
import paho.mqtt.client as mqtt
from asyncua import Server
from machines.cnc_machine import CNCMachine
from machines.conveyor import ConveyorBelt
from machines.robot_arm import RobotArm

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "machines.yaml")

MACHINE_CLASSES = {
    "cnc": CNCMachine,
    "conveyor": ConveyorBelt,
    "robot_arm": RobotArm,
}


def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def build_mqtt_client(broker: str, port: int, client_id: str) -> mqtt.Client:
    client = mqtt.Client(client_id=client_id)
    client.connect(broker, port, keepalive=60)
    client.loop_start()
    return client


async def main():
    cfg = load_config()
    mqtt_cfg = cfg["mqtt"]
    broker = os.getenv("MQTT_BROKER", mqtt_cfg.get("broker", "localhost"))
    port = int(os.getenv("MQTT_PORT", str(mqtt_cfg.get("port", 1883))))

    mqtt_client = build_mqtt_client(broker, port, mqtt_cfg["client_id"])

    async def publish(topic: str, payload: str):
        mqtt_client.publish(topic, payload, qos=mqtt_cfg.get("qos", 1))

    # OPC-UA server setup
    ua_server = Server()
    await ua_server.init()
    ua_server.set_endpoint(cfg["opcua"]["endpoint"])
    await ua_server.start()

    machines = []
    for m_cfg in cfg["machines"]:
        cls = MACHINE_CLASSES[m_cfg["type"]]
        machines.append(cls(
            machine_id=m_cfg["id"],
            name=m_cfg["name"],
            mqtt_topic=m_cfg["mqtt_topic"],
            update_interval_ms=m_cfg["update_interval_ms"],
        ))

    print(f"OPC-UA server running at {cfg['opcua']['endpoint']}")
    print(f"Publishing to MQTT broker {broker}:{port}")

    await asyncio.gather(*[m.run(publish) for m in machines])


if __name__ == "__main__":
    asyncio.run(main())
