from odoo import api, fields, models


class EmployeePenalty(models.Model):
    _name = 'employee.penalty'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char()
    penalty_type_id = fields.Many2one(comodel_name="employee.penalty.type", string="Type")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    department_id = fields.Many2one(related="employee_id.department_id", store=True)
    job_id = fields.Many2one(related="employee_id.job_id", store=True)
    date = fields.Date(default=fields.Date.today())
    penalty_by = fields.Selection(string="Penalty Type",
                                  selection=[('hour', 'Hour'), ('day', 'Day'), ('amount', 'Amount')], default='amount')
    penalty_value = fields.Float()
    amount = fields.Float(compute='compute_penalty_amount',store=True)
    reason = fields.Text()
    state = fields.Selection(selection=[('draft', 'Draft'), ('submit', 'Submit'), ('approved', 'Approved')],
                             default='draft')

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, "%s [%s]" % (rec.penalty_type_id.name, rec.employee_id.name)))
        return result

    @api.depends('penalty_by','penalty_value',
                 'employee_id.contract_id.hour_value',
                 'employee_id.contract_id.day_value')
    def compute_penalty_amount(self):
        for rec in self:
            if rec.penalty_by == 'hour':
                rec.amount = rec.penalty_value * rec.employee_id.contract_id.hour_value
            elif rec.penalty_by == 'day':
                rec.amount = rec.penalty_value * rec.employee_id.contract_id.day_value
            else:
                rec.amount = rec.penalty_value

    def button_submit(self):
        self.state = 'submit'

    def button_approve(self):
        self.state = 'approved'
