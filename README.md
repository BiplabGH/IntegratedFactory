# IntegratedFactory

End-to-end Industrial IoT platform simulating a connected factory with OPC-UA machines, 
unified namespace (UNS), MES integration, cloud sync, and agentic AI.

## Architecture Overview

```
OPC-UA Machines
     │
     ▼
MQTT (EMQX) ──► Solace PubSub+ (UNS)
     │
     ▼
Apache Kafka (streaming backbone)
     │
     ├──► InfluxDB (raw historian)
     └──► TimescaleDB (aggregated)
     │
     ├──► Odoo MES
     │
     ▼
MCP Server (tool exposure)
     │
     ▼
A2A AI Agents (quality, maintenance, production)
     │
     ▼
Azure Cloud (IoT Hub, Event Hubs, ADX)
```

## Components

| Directory          | Description                                      |
|--------------------|--------------------------------------------------|
| `opcua-simulator/` | Python OPC-UA server simulating factory machines |
| `mqtt-broker/`     | EMQX config, Solace PubSub+ config, MQTT bridge  |
| `kafka/`           | Kafka config, connectors, stream processors      |
| `historian/`       | InfluxDB + TimescaleDB writers and migrations    |
| `mes/`             | Odoo MES custom addon + Kafka connector          |
| `mcp-server/`      | TypeScript MCP server exposing factory tools     |
| `agents/`          | Python A2A AI agents (quality/maintenance/prod)  |
| `iac/`             | Service YAML definitions for local deployment   |
| `k8s/`             | Helm chart for Kubernetes deployment            |
| `azure/`           | Bicep IaC, Azure Pipelines CI/CD                |
| `docs/`            | Architecture, data flow, API reference docs     |

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+
- Python 3.11+
- kubectl + Helm 3

### Local Development

```bash
# Start core infrastructure
docker-compose up -d

# Start OPC-UA simulator
cd opcua-simulator && pip install -r requirements.txt
python src/server.py

# Start MCP server
cd mcp-server && npm install && npm run dev

# Start AI agents
cd agents && pip install -r requirements.txt
python src/orchestrator.py
```

## Data Flow

See [docs/data-flow.md](docs/data-flow.md) for detailed data flow documentation.

## Contributing

See [docs/getting-started.md](docs/getting-started.md) for development setup.
