import json
import os
import logging
from datetime import datetime, timezone
import psycopg2
from confluent_kafka import Consumer, KafkaError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("timescale-writer")

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
TIMESCALE_URL = os.getenv("TIMESCALE_URL", "postgresql://factory:factory-pass@localhost:5432/factory_agg")

INSERT_SQL = """
INSERT INTO machine_metrics (time, machine_id, machine_type, metric_name, value)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
"""


def main():
    conn = psycopg2.connect(TIMESCALE_URL)
    conn.autocommit = True

    consumer = Consumer({
        "bootstrap.servers": KAFKA_BOOTSTRAP,
        "group.id": "timescale-writer",
        "auto.offset.reset": "earliest",
    })
    consumer.subscribe(["factory.aggregated.metrics"])

    logger.info("TimescaleDB writer started")

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
                ts = datetime.fromtimestamp(data["window_end"], tz=timezone.utc)
                machine_id = data["machine_id"]
                machine_type = machine_id.split("_")[0] if "_" in machine_id else "unknown"

                rows = [
                    (ts, machine_id, machine_type, metric, stats["avg"])
                    for metric, stats in data.get("telemetry", {}).items()
                    if isinstance(stats, dict) and "avg" in stats
                ]

                with conn.cursor() as cur:
                    cur.executemany(INSERT_SQL, rows)
            except Exception as e:
                logger.error("Write error: %s", e)
    finally:
        consumer.close()
        conn.close()


if __name__ == "__main__":
    main()
