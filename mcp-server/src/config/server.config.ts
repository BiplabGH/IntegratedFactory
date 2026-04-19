import 'dotenv/config';

export const config = {
  influxdb: {
    url: process.env.INFLUXDB_URL ?? 'http://localhost:8086',
    token: process.env.INFLUXDB_TOKEN ?? 'factory-dev-token',
    org: process.env.INFLUXDB_ORG ?? 'IntegratedFactory',
    rawBucket: 'raw_historian',
    aggBucket: 'aggregated_historian',
  },
  timescale: {
    connectionString:
      process.env.TIMESCALE_URL ??
      'postgresql://factory:factory-pass@localhost:5432/factory_agg',
  },
  kafka: {
    brokers: (process.env.KAFKA_BOOTSTRAP ?? 'localhost:9092').split(','),
  },
  server: {
    port: parseInt(process.env.PORT ?? '3000', 10),
  },
};
