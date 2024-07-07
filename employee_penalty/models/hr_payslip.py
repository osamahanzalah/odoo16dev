from odoo import api, fields, models


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    penalty_ids = fields.Many2many(comodel_name="employee.penalty", string="Employee Penalties", )
    penalty_amount = fields.Float(compute="compute_penalty_amount",store=True)
    allowances_ids = fields.Many2many(comodel_name="employee.allowances", string="Employee Allowances", )
    allowances_amount = fields.Float(compute="compute_allowances_amount",store=True)

    @api.onchange('employee_id', 'date_from', 'date_to')
    def get_employee_penalty(self):
        penalty = self.env['employee.penalty'].search([('employee_id','=',self.employee_id.id),('date','>=',self.date_from),
                                             ('date','<=',self.date_to),('state','=','approved')])
        allowances = self.env['employee.allowances'].search([('employee_id','=',self.employee_id.id),('date','>=',self.date_from),
                                             ('date','<=',self.date_to),('state','=','approved')])
        self.penalty_ids = penalty.ids
        self.allowances_ids = allowances.ids

    @api.depends('penalty_ids')
    def compute_penalty_amount(self):
        for rec in self:
            rec.penalty_amount = sum(rec.penalty_ids.mapped('amount'))

    @api.depends('allowances_ids')
    def compute_allowances_amount(self):
        for rec in self:
            rec.allowances_amount = sum(rec.allowances_ids.mapped('amount'))