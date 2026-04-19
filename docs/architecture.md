# Architecture

## System Overview

IntegratedFactory is a layered Industrial IoT platform following the ISA-95 hierarchy.

```
Level 0-1: Physical / Sensor
  └── Simulated OPC-UA machines (CNC, Conveyor, Robot Arm)

Level 2: Control / Edge
  └── EMQX MQTT Broker
      └── MQTT → Kafka Bridge

Level 3: MES
  ├── Apache Kafka (streaming backbone)
  ├── Solace PubSub+ (Unified Namespace / ISA-95 topic hierarchy)
  └── Odoo (Manufacturing Execution System)

Level 4: Operations
  ├── InfluxDB (raw time-series historian)
  ├── TimescaleDB (aggregated metrics, continuous aggregates)
  └── MCP Server (AI tool exposure)

Level 5: Enterprise / Cloud
  ├── A2A AI Agents (Quality, Maintenance, Production)
  └── Azure (IoT Hub, Event Hubs, AKS)
```

## Component Interactions

### Data Ingestion Path
1. OPC-UA simulator generates telemetry every 250–1000 ms per machine.
2. Telemetry is published to EMQX on `factory/machines/{type}/{id}`.
3. MQTT Bridge subscribes to `factory/#` and forwards to Kafka topics.
4. Kafka Connect InfluxDB Sink writes raw records to InfluxDB.
5. Historian Writer additionally writes 1-minute aggregates to TimescaleDB.

### UNS Path (Solace)
- EMQX bridges `factory/#` to Solace PubSub+ following the ISA-95 topic model:
  `factory/{enterprise}/{site}/{area}/{line}/{machine}/{datatype}`

### AI Agent Path
1. Agents call MCP Server tools (`get_raw_historian`, `list_machines`, etc.).
2. MCP Server queries InfluxDB (raw) and TimescaleDB (aggregated).
3. Agent sends Claude API request with tool definitions.
4. Claude drives multi-turn tool-use loops to produce assessments.

## Technology Decisions

| Concern                  | Choice            | Reason                                          |
|--------------------------|-------------------|-------------------------------------------------|
| Time-series raw          | InfluxDB          | High-frequency writes, Flux query language      |
| Time-series aggregated   | TimescaleDB       | SQL interface, continuous aggregates, joins MES |
| Streaming backbone       | Kafka             | Durable, replayable, connector ecosystem        |
| MQTT broker              | EMQX              | Production-grade, clustering, rule engine       |
| UNS                      | Solace PubSub+    | ISA-95 compliant, event mesh                   |
| MES                      | Odoo              | Open-source ERP/MES with Python extensibility   |
| AI tool exposure         | MCP               | Standard protocol for LLM tool integration      |
| AI backbone              | Claude / Anthropic| claude-sonnet-4-6, tool use, async              |
