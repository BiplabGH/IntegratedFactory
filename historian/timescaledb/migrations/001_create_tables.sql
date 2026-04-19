CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS machine_metrics (
    time        TIMESTAMPTZ NOT NULL,
    machine_id  TEXT        NOT NULL,
    machine_type TEXT       NOT NULL,
    metric_name TEXT        NOT NULL,
    value       DOUBLE PRECISION,
    unit        TEXT
);

SELECT create_hypertable('machine_metrics', 'time', if_not_exists => TRUE);

CREATE INDEX IF NOT EXISTS idx_machine_metrics_machine_id ON machine_metrics (machine_id, time DESC);
CREATE INDEX IF NOT EXISTS idx_machine_metrics_metric_name ON machine_metrics (metric_name, time DESC);
