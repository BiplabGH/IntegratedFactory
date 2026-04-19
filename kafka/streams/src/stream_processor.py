import json
import os
import logging
from confluent_kafka import Consumer, Producer, KafkaError
from aggregator import Aggregator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("stream-processor")

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
INPUT_TOPICS = ["factory.machines.cnc", "factory.machines.conveyor", "factory.machines.robot"]
OUTPUT_TOPIC = "factory.aggregated.metrics"


def main():
    consumer = Consumer({
        "bootstrap.servers": KAFKA_BOOTSTRAP,
        "group.id": "factory-stream-processor",
        "auto.offset.reset": "earliest",
    })
    producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})
    aggregator = Aggregator(window_seconds=60)

    consumer.subscribe(INPUT_TOPICS)
    logger.info("Stream processor consuming from %s", INPUT_TOPICS)

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
                aggregated = aggregator.process(data)
                if aggregated:
                    producer.produce(OUTPUT_TOPIC, value=json.dumps(aggregated).encode())
                    producer.poll(0)
            except json.JSONDecodeError as e:
                logger.warning("Invalid JSON: %s", e)
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
