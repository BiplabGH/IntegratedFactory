import json
import logging
from confluent_kafka import Consumer, KafkaError
from odoo_connector import OdooConnector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mes-sync")

import os
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")


def main():
    odoo = OdooConnector()
    consumer = Consumer({
        "bootstrap.servers": KAFKA_BOOTSTRAP,
        "group.id": "mes-sync",
        "auto.offset.reset": "latest",
    })
    consumer.subscribe(["factory.machines.cnc", "factory.machines.conveyor", "factory.machines.robot"])

    logger.info("MES sync started")

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    logger.error("Consumer error: %s", msg.error())
                continue

            try:
                data = json.loads(msg.value())
                odoo.upsert_machine_status(
                    machine_id=data["machine_id"],
                    is_running=data.get("running", False),
                    error_code=data.get("error_code", 0),
                    telemetry_json=json.dumps(data.get("telemetry", {})),
                )
            except Exception as e:
                logger.error("Sync error: %s", e)
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
