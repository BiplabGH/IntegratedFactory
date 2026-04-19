-- 1-minute continuous aggregate
CREATE MATERIALIZED VIEW IF NOT EXISTS machine_metrics_1min
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 minute', time) AS bucket,
    machine_id,
    metric_name,
    AVG(value)  AS avg_value,
    MIN(value)  AS min_value,
    MAX(value)  AS max_value,
    COUNT(*)    AS sample_count
FROM machine_metrics
GROUP BY bucket, machine_id, metric_name
WITH NO DATA;

SELECT add_continuous_aggregate_policy('machine_metrics_1min',
    start_offset => INTERVAL '10 minutes',
    end_offset   => INTERVAL '1 minute',
    schedule_interval => INTERVAL '1 minute');

-- 1-hour continuous aggregate
CREATE MATERIALIZED VIEW IF NOT EXISTS machine_metrics_1hour
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    machine_id,
    metric_name,
    AVG(value)  AS avg_value,
    MIN(value)  AS min_value,
    MAX(value)  AS max_value,
    COUNT(*)    AS sample_count
FROM machine_metrics
GROUP BY bucket, machine_id, metric_name
WITH NO DATA;

SELECT add_continuous_aggregate_policy('machine_metrics_1hour',
    start_offset => INTERVAL '2 hours',
    end_offset   => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour');
