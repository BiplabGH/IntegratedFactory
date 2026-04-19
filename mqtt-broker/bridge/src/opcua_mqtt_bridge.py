import os
import json
import logging
from confluent_kafka import Producer
import paho.mqtt.client as mqtt
from topic_mapper import mqtt_to_kafka_topic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mqtt-bridge")

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")

producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})


def on_message(client, userdata, msg):
    kafka_topic = mqtt_to_kafka_topic(msg.topic)
    try:
        producer.produce(
            kafka_topic,
            key=msg.topic.encode(),
            value=msg.payload,
        )
        producer.poll(0)
    except Exception as e:
        logger.error("Failed to produce to Kafka: %s", e)


def main():
    client = mqtt.Client(client_id="mqtt-bridge")
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.subscribe("factory/#", qos=1)
    logger.info("MQTT bridge connected to %s:%d, forwarding to Kafka %s", MQTT_BROKER, MQTT_PORT, KAFKA_BOOTSTRAP)
    client.loop_forever()


if __name__ == "__main__":
    main()
