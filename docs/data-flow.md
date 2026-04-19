# Data Flow

## Message Schema

Every machine publishes a JSON payload with this structure:

```json
{
  "machine_id": "cnc_001",
  "machine_type": "cnc",
  "timestamp": 1713542400.123,
  "running": true,
  "error_code": 0,
  "telemetry": {
    "spindle_speed_rpm": 3012.4,
    "feed_rate_mm_min": 498.7,
    "tool_wear_percent": 23.5,
    "coolant_temp_c": 24.8,
    "vibration_mm_s": 0.47,
    "parts_produced": 2
  }
}
```

## MQTT Topic Hierarchy

```
factory/
└── machines/
    ├── cnc/
    │   └── 001          ← cnc_001 raw telemetry
    ├── conveyor/
    │   └── 001
    └── robot/
        └── 001
```

## Kafka Topic Mapping

| MQTT Topic                     | Kafka Topic                  |
|--------------------------------|------------------------------|
| `factory/machines/cnc/#`       | `factory.machines.cnc`       |
| `factory/machines/conveyor/#`  | `factory.machines.conveyor`  |
| `factory/machines/robot/#`     | `factory.machines.robot`     |
| Stream Processor output        | `factory.aggregated.metrics` |
| Agent-generated alerts         | `factory.alerts`             |

## UNS (ISA-95) via Solace

Solace bridges and re-publishes using the full ISA-95 topic hierarchy:

```
factory/{enterprise}/{site}/{area}/{line}/{machine}/{datatype}
factory/plant1/area_a/machining/line1/cnc_001/telemetry
```

## Retention Policy

| Store          | Retention         | Notes                              |
|----------------|-------------------|------------------------------------|
| InfluxDB raw   | 1 day             | High-frequency, volatile           |
| InfluxDB agg   | 90 days           | Downsampled                        |
| TimescaleDB 1m | chunk compression | Continuous aggregate, SQL queryable |
| TimescaleDB 1h | chunk compression | Long-term trend analysis            |
| Kafka          | 1–30 days         | Per-topic, configurable            |
