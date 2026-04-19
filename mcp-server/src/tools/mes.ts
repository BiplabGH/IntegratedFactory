import { Pool } from 'pg';
import xmlrpc from 'xmlrpc';
import { config } from '../config/server.config.js';

const ODOO_URL = process.env.ODOO_URL ?? 'http://localhost:8069';
const ODOO_DB = process.env.ODOO_DB ?? 'integrated_factory_mes';
const ODOO_USER = process.env.ODOO_USER ?? 'admin';
const ODOO_PASS = process.env.ODOO_PASSWORD ?? 'admin';

async function odooAuthenticate(): Promise<number> {
  return new Promise((resolve, reject) => {
    const client = xmlrpc.createClient({ url: `${ODOO_URL}/xmlrpc/2/common` });
    client.methodCall('authenticate', [ODOO_DB, ODOO_USER, ODOO_PASS, {}], (err, uid) => {
      if (err) reject(err);
      else resolve(uid as number);
    });
  });
}

export async function getActiveWorkOrders(): Promise<object[]> {
  const uid = await odooAuthenticate();
  return new Promise((resolve, reject) => {
    const client = xmlrpc.createClient({ url: `${ODOO_URL}/xmlrpc/2/object` });
    client.methodCall(
      'execute_kw',
      [ODOO_DB, uid, ODOO_PASS, 'mrp.workorder', 'search_read',
        [[['state', 'in', ['ready', 'progress']]]],
        { fields: ['name', 'state', 'machine_id', 'workcenter_id', 'date_planned_start'] }
      ],
      (err, result) => {
        if (err) reject(err);
        else resolve(result as object[]);
      }
    );
  });
}
