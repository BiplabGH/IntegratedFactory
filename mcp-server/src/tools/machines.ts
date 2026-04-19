import { Pool } from 'pg';
import { config } from '../config/server.config.js';

const pool = new Pool({ connectionString: config.timescale.connectionString });

export async function getMachineList(): Promise<object[]> {
  const result = await pool.query(
    `SELECT DISTINCT machine_id, machine_type, MAX(time) AS last_seen
     FROM machine_metrics
     GROUP BY machine_id, machine_type
     ORDER BY last_seen DESC`
  );
  return result.rows;
}

export async function getMachineLatestMetrics(machineId: string): Promise<object[]> {
  const result = await pool.query(
    `SELECT metric_name, value, time
     FROM machine_metrics
     WHERE machine_id = $1
       AND time > NOW() - INTERVAL '5 minutes'
     ORDER BY time DESC`,
    [machineId]
  );
  return result.rows;
}

export async function getMachineMetricHistory(
  machineId: string,
  metricName: string,
  hours: number = 1
): Promise<object[]> {
  const result = await pool.query(
    `SELECT bucket, avg_value, min_value, max_value, sample_count
     FROM machine_metrics_1min
     WHERE machine_id = $1
       AND metric_name = $2
       AND bucket > NOW() - ($3 || ' hours')::interval
     ORDER BY bucket ASC`,
    [machineId, metricName, hours]
  );
  return result.rows;
}
