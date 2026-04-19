# MCP Server API Reference

The MCP Server exposes factory data to AI agents via the Model Context Protocol.

## Tools

### `get_raw_historian`
Query raw time-series telemetry from InfluxDB.

**Input:**
```json
{
  "machine_id": "cnc_001",
  "minutes": 60
}
```

---

### `get_aggregated_metrics`
Query aggregated metrics (mean) over a time window from InfluxDB.

**Input:**
```json
{
  "machine_id": "cnc_001",
  "metric": "spindle_speed_rpm",
  "window_minutes": 60
}
```

---

### `list_machines`
List all machines with their last-seen timestamp from TimescaleDB.

**Input:** `{}`

---

### `get_machine_latest_metrics`
Get all metric readings for a machine in the last 5 minutes.

**Input:**
```json
{
  "machine_id": "cnc_001"
}
```

---

### `get_machine_metric_history`
Get 1-minute aggregated history for a specific metric.

**Input:**
```json
{
  "machine_id": "cnc_001",
  "metric_name": "tool_wear_percent",
  "hours": 8
}
```

---

### `get_active_work_orders`
Retrieve active work orders from Odoo MES.

**Input:** `{}`

---

## Resources

### `factory://schema`
Returns the full factory schema including machine types, topic patterns, Kafka topics, and available metrics per machine type.

## Agents

| Agent              | Purpose                                   | Poll Interval |
|--------------------|-------------------------------------------|---------------|
| QualityAgent       | Detect tool wear and vibration anomalies  | 30 s          |
| MaintenanceAgent   | Predict maintenance needs from trends     | 5 min         |
| ProductionAgent    | Monitor work order progress vs. machines  | 60 s          |
