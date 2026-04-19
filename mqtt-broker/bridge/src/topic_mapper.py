def mqtt_to_kafka_topic(mqtt_topic: str) -> str:
    """Map MQTT topic hierarchy to a Kafka topic name.

    factory/machines/cnc/001  →  factory.machines.cnc
    """
    parts = mqtt_topic.split("/")
    # Use first 3 segments as Kafka topic, replace / with .
    kafka_topic = ".".join(parts[:3]) if len(parts) >= 3 else mqtt_topic.replace("/", ".")
    return kafka_topic
