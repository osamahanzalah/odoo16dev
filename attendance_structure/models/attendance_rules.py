from odoo import api, fields, models
import time

class AttendanceRuleLine(models.Model):
    _name = 'attendance.deduction.rules.line'

    rule_id = fields.Many2one(comodel_name="attendance.deduction.rules",)
    repetition = fields.Integer(required=True,default=1)
    apply_hours = fields.Float(string="Apply Deduction(Hours)",  required=False, )
    apply_days = fields.Float(string="Apply Deduction(Days)",  required=False, )


class AttendanceRules(models.Model):
    _name = 'attendance.deduction.rules'
    _rec_name = 'name'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']


    name = fields.Char(compute="compute_name")
    duration_type = fields.Selection(selection=[('late', 'Late Check In'),
                                                ('early', 'Early Checkout'),
                                                ('absent', 'Absent'), ], default='late', required=True, )
    remaining = fields.Boolean(string="Actual Late Minutes", )
    from_time = fields.Float(string="From", required=False, )
    to_time = fields.Float(string="To", required=False, )
    penalty_base = fields.Selection(selection=[('hour', 'Hour'), ('day', 'Day'), ], default='day', required=True, )
    line_ids = fields.One2many(comodel_name="attendance.deduction.rules.line", inverse_name="rule_id",)

    @api.depends('duration_type','from_time','to_time')
    def compute_name(self):
        for rec in self:
            if rec.duration_type != 'absent':
                from_time = '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.from_time * 60, 60))
                to_time = '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.to_time * 60, 60))
                rec.name = "Time " + str(rec.duration_type) + " From (" + from_time + ") To (" + to_time + ")"
            else:
                rec.name = "Absent Rule"

    def get_penalty(self,repetition,hours_per_day,actual_hours=0.0):
        if self.remaining and not self.duration_type == 'absent':
            return actual_hours
        res = self.line_ids.filtered(lambda x: x.repetition == repetition)
        if res:
            if self.penalty_base == 'hour':
                return res.apply_hours
            else:
                return res.apply_days * hours_per_day
        else:
            res = self.line_ids.sorted(key='repetition')[-1]
            if repetition > res.repetition:
                if self.penalty_base == 'hour':
                    return res.apply_hours
                else:
                    return res.apply_days * hours_per_day
            else:
                return 0.0

