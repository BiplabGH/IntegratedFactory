import { InfluxDB } from '@influxdata/influxdb-client';
import { config } from '../config/server.config.js';

const influx = new InfluxDB({ url: config.influxdb.url, token: config.influxdb.token });

export async function queryRawHistorian(machineId: string, minutes: number = 60): Promise<object[]> {
  const queryApi = influx.getQueryApi(config.influxdb.org);
  const flux = `
    from(bucket: "${config.influxdb.rawBucket}")
      |> range(start: -${minutes}m)
      |> filter(fn: (r) => r["machine_id"] == "${machineId}")
      |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
      |> limit(n: 1000)
  `;

  const rows: object[] = [];
  await queryApi.collectRows(flux, (row, tableMeta) => {
    rows.push(tableMeta.toObject(row));
  });
  return rows;
}

export async function queryAggregatedMetrics(
  machineId: string,
  metric: string,
  windowMinutes: number = 60
): Promise<object[]> {
  const queryApi = influx.getQueryApi(config.influxdb.org);
  const flux = `
    from(bucket: "${config.influxdb.aggBucket}")
      |> range(start: -${windowMinutes}m)
      |> filter(fn: (r) => r["machine_id"] == "${machineId}" and r["_field"] == "${metric}")
      |> mean()
  `;

  const rows: object[] = [];
  await queryApi.collectRows(flux, (row, tableMeta) => {
    rows.push(tableMeta.toObject(row));
  });
  return rows;
}
