from odoo import api, fields, models


class PayslipLine(models.Model):
    _inherit = 'hr.payslip.line'

    batch_id = fields.Many2one(related="slip_id.payslip_run_id",store=True,string="Batch")
