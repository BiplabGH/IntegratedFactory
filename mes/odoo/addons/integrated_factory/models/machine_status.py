from odoo import fields, models


class MachineStatus(models.Model):
    _name = "integrated_factory.machine_status"
    _description = "Real-time Machine Status from OPC-UA"
    _order = "last_updated desc"

    machine_id = fields.Char(string="Machine ID", required=True, index=True)
    machine_type = fields.Char(string="Machine Type")
    last_updated = fields.Datetime(string="Last Updated")
    is_running = fields.Boolean(string="Running", default=False)
    error_code = fields.Integer(string="Error Code", default=0)
    telemetry_json = fields.Text(string="Telemetry (JSON)")

    _sql_constraints = [
        ("machine_id_unique", "UNIQUE(machine_id)", "Machine ID must be unique"),
    ]
