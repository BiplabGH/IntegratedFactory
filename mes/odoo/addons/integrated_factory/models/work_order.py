from odoo import fields, models


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    machine_id = fields.Char(string="OPC-UA Machine ID")
    machine_status_id = fields.Many2one(
        "integrated_factory.machine_status",
        string="Live Machine Status",
        compute="_compute_machine_status",
        store=False,
    )

    def _compute_machine_status(self):
        for record in self:
            record.machine_status_id = self.env["integrated_factory.machine_status"].search(
                [("machine_id", "=", record.machine_id)], limit=1
            )
