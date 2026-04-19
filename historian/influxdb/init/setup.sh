#!/bin/bash
# Called automatically by the InfluxDB Docker entrypoint if DOCKER_INFLUXDB_INIT_MODE=setup
# Additional bucket and retention setup runs here after initialization.

INFLUX="influx --host http://localhost:8086 --token ${DOCKER_INFLUXDB_INIT_ADMIN_TOKEN}"

# Aggregated bucket with 90-day retention
$INFLUX bucket create \
  --org IntegratedFactory \
  --name aggregated_historian \
  --retention 2160h  # 90 days

echo "InfluxDB setup complete"
