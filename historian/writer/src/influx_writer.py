import json
import os
import logging
from datetime import datetime, timezone
from confluent_kafka import Consumer, KafkaError
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("influx-writer")

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "factory-dev-token")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "IntegratedFactory")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "raw_historian")


def flatten_telemetry(telemetry: dict, prefix: str = "") -> dict[str, float]:
    """Recursively flatten nested telemetry dict to {field: value} pairs."""
    result = {}
    for k, v in telemetry.items():
        key = f"{prefix}{k}" if not prefix else f"{prefix}_{k}"
        if isinstance(v, dict):
            result.update(flatten_telemetry(v, key))
        elif isinstance(v, (int, float)):
            result[key] = float(v)
    return result


def main():
    influx = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    write_api = influx.write_api(write_options=SYNCHRONOUS)

    consumer = Consumer({
        "bootstrap.servers": KAFKA_BOOTSTRAP,
        "group.id": "influx-writer",
        "auto.offset.reset": "earliest",
    })
    consumer.subscribe(["factory.machines.cnc", "factory.machines.conveyor", "factory.machines.robot"])

    logger.info("InfluxDB writer started, writing to bucket %s", INFLUXDB_BUCKET)

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
                ts = datetime.fromtimestamp(data["timestamp"], tz=timezone.utc)
                fields = flatten_telemetry(data.get("telemetry", {}))

                point = (
                    Point(data["machine_type"])
                    .tag("machine_id", data["machine_id"])
                    .time(ts, WritePrecision.NANOSECONDS)
                )
                for field, value in fields.items():
                    point.field(field, value)

                write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            except Exception as e:
                logger.error("Write error: %s", e)
    finally:
        consumer.close()
        influx.close()


if __name__ == "__main__":
    main()
