# Getting Started

## Prerequisites

| Tool               | Version   |
|--------------------|-----------|
| Docker             | 24+       |
| Docker Compose     | 2.24+     |
| Python             | 3.11+     |
| Node.js            | 20+       |
| kubectl            | 1.29+     |
| Helm               | 3.14+     |
| Azure CLI          | 2.60+     |

## Local Development Setup

### 1. Clone and configure

```bash
git clone https://github.com/biplabgh/IntegratedFactory
cd IntegratedFactory
cp .env.example .env   # fill in ANTHROPIC_API_KEY
```

### 2. Start infrastructure

```bash
docker-compose up -d emqx zookeeper kafka influxdb timescaledb
```

Wait for all services to be healthy:
```bash
docker-compose ps
```

### 3. Start OPC-UA Simulator

```bash
cd opcua-simulator
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/server.py
```

### 4. Start MQTT Bridge

```bash
cd mqtt-broker/bridge
pip install -r requirements.txt
python src/opcua_mqtt_bridge.py
```

### 5. Start Historian Writer

```bash
cd historian/writer
pip install -r requirements.txt
python src/influx_writer.py &
python src/timescale_writer.py &
```

### 6. Start MCP Server

```bash
cd mcp-server
npm install
npm run dev
```

### 7. Start AI Agents

```bash
cd agents
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
python src/orchestrator.py
```

## Verifying the Stack

| Service        | URL                            | Credentials          |
|----------------|--------------------------------|----------------------|
| EMQX Dashboard | http://localhost:18083         | admin / factory-admin |
| InfluxDB UI    | http://localhost:8086          | admin / factory-admin |
| Odoo MES       | http://localhost:8069          | admin / admin        |

## Running on Kubernetes (AKS)

```bash
# Deploy Azure infra
cd azure && bash scripts/deploy.sh

# Install Helm chart
helm upgrade --install integrated-factory k8s/ \
  -f k8s/values-prod.yaml \
  --namespace factory \
  --create-namespace \
  --wait
```
