from odoo import api, fields, models


class EmployeeAllowances(models.Model):
    _name = 'employee.allowances'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char()
    allowances_type_id = fields.Many2one(comodel_name="employee.allowances.type", string="Type")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    department_id = fields.Many2one(related="employee_id.department_id", store=True)
    job_id = fields.Many2one(related="employee_id.job_id", store=True)
    date = fields.Date(default=fields.Date.today())
    allowances_by = fields.Selection(string="Allowances Type",
                                  selection=[('hour', 'Hour'), ('day', 'Day'), ('amount', 'Amount')], default='amount')
    allowances_value = fields.Float()
    amount = fields.Float(compute='compute_allowances_amount',store=True)
    reason = fields.Text()
    state = fields.Selection(selection=[('draft', 'Draft'), ('submit', 'Submit'), ('approved', 'Approved')],
                             default='draft')

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, "%s [%s]" % (rec.allowances_type_id.name, rec.employee_id.name)))
        return result

    @api.depends('allowances_by','allowances_value',
                 'employee_id.contract_id.hour_value',
                 'employee_id.contract_id.day_value')
    def compute_allowances_amount(self):
        for rec in self:
            if rec.allowances_by == 'hour':
                rec.amount = rec.allowances_value * rec.employee_id.contract_id.hour_value
            elif rec.allowances_by == 'day':
                rec.amount = rec.allowances_value * rec.employee_id.contract_id.day_value
            else:
                rec.amount = rec.allowances_value

    def button_submit(self):
        self.state = 'submit'

    def button_approve(self):
        self.state = 'approved'
