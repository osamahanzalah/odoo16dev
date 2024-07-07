from odoo import api, fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    employee_type_id = fields.Many2one(related="employee_id.employee_type_id",store=True)
    day_value = fields.Float(compute="compute_day_value")
    hour_value = fields.Float()
    no_month_days = fields.Float(string="No. Month Days",  default=30)
    workday_hours = fields.Integer(default=8)

    @api.depends('no_month_days','workday_hours')
    def compute_day_value(self):
        for rec in self:
            rec.day_value = rec.wage / rec.no_month_days if rec.no_month_days > 0 else 0
            rec.hour_value = rec.day_value / rec.workday_hours if rec.workday_hours > 0 else 0