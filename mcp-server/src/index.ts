import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { queryRawHistorian, queryAggregatedMetrics } from './tools/historian.js';
import { getMachineList, getMachineLatestMetrics, getMachineMetricHistory } from './tools/machines.js';
import { getActiveWorkOrders } from './tools/mes.js';
import { FACTORY_SCHEMA } from './resources/factory-schema.js';

const server = new McpServer({
  name: 'integrated-factory',
  version: '1.0.0',
});

// ── Historian tools ──────────────────────────────────────────────────────────
server.tool(
  'get_raw_historian',
  'Query raw time-series data for a machine from InfluxDB',
  {
    machine_id: z.string().describe('Machine ID, e.g. cnc_001'),
    minutes: z.number().min(1).max(1440).default(60).describe('Lookback window in minutes'),
  },
  async ({ machine_id, minutes }) => {
    const rows = await queryRawHistorian(machine_id, minutes);
    return { content: [{ type: 'text', text: JSON.stringify(rows, null, 2) }] };
  }
);

server.tool(
  'get_aggregated_metrics',
  'Query aggregated metrics from InfluxDB',
  {
    machine_id: z.string(),
    metric: z.string().describe('Metric name, e.g. spindle_speed_rpm'),
    window_minutes: z.number().default(60),
  },
  async ({ machine_id, metric, window_minutes }) => {
    const rows = await queryAggregatedMetrics(machine_id, metric, window_minutes);
    return { content: [{ type: 'text', text: JSON.stringify(rows, null, 2) }] };
  }
);

// ── Machine tools ─────────────────────────────────────────────────────────────
server.tool(
  'list_machines',
  'List all machines with their last-seen timestamp from TimescaleDB',
  {},
  async () => {
    const machines = await getMachineList();
    return { content: [{ type: 'text', text: JSON.stringify(machines, null, 2) }] };
  }
);

server.tool(
  'get_machine_latest_metrics',
  'Get the latest metric readings for a machine (last 5 minutes)',
  { machine_id: z.string() },
  async ({ machine_id }) => {
    const metrics = await getMachineLatestMetrics(machine_id);
    return { content: [{ type: 'text', text: JSON.stringify(metrics, null, 2) }] };
  }
);

server.tool(
  'get_machine_metric_history',
  'Get 1-minute aggregated metric history from TimescaleDB',
  {
    machine_id: z.string(),
    metric_name: z.string(),
    hours: z.number().min(1).max(168).default(1),
  },
  async ({ machine_id, metric_name, hours }) => {
    const history = await getMachineMetricHistory(machine_id, metric_name, hours);
    return { content: [{ type: 'text', text: JSON.stringify(history, null, 2) }] };
  }
);

// ── MES tools ─────────────────────────────────────────────────────────────────
server.tool(
  'get_active_work_orders',
  'Retrieve active work orders from Odoo MES',
  {},
  async () => {
    const orders = await getActiveWorkOrders();
    return { content: [{ type: 'text', text: JSON.stringify(orders, null, 2) }] };
  }
);

// ── Schema resource ───────────────────────────────────────────────────────────
server.resource(
  'factory-schema',
  'factory://schema',
  async () => ({
    contents: [{ uri: 'factory://schema', text: JSON.stringify(FACTORY_SCHEMA, null, 2) }],
  })
);

const transport = new StdioServerTransport();
await server.connect(transport);
console.error('IntegratedFactory MCP server running on stdio');
