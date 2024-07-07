# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Cycle(models.Model):
    _name = 'cycle.config'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'name'


    name = fields.Char('Description')
    cycle_code = fields.Char('Cycle ID', readonly=True, store=True,track_visibility='onchange')
    type = fields.Selection(string="Type",
                                    selection=[
                                        ('general_cycle', 'General cycle'),
                                        ('private_cycle', 'Private cycle'),
                                        ('company_cycle', 'Company cycle'),
                                    ],
                                    required=False, track_visibility='onchange')
    months_no = fields.Integer('Number of months',track_visibility='onchange')
    date_start = fields.Date(string="Start Date", required=False,track_visibility='onchange' )
    date_end = fields.Date(string="End Date", required=False,track_visibility='onchange' )
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Ambassador", required=False,track_visibility='onchange' )
    agent_id = fields.Many2one(comodel_name="hr.employee", string="Follow-up agent", required=False, track_visibility='onchange')

    state = fields.Selection(string="Status",track_visibility='onchange', selection=[('draft', 'Draft'), ('active', 'Active'),('ended', 'Ended'), ], required=False,default='draft' )

    line_ids = fields.One2many(comodel_name="cycle.config.line", inverse_name="cycle_id", string="", required=False, )
    ambassador_commission = fields.Float('Ambassador commission')
    def button_active(self):
        self.state='active'
    @api.constrains('date_start', 'date_end')
    def _check_date(self):
        if self.date_start and self.date_end:
            if self.date_start > self.date_end:
                raise ValidationError(_('Start Date must be less than End date!'))

    # @api.model
    # def create(self, values):
    #     values['name'] = self.env['ir.sequence'].next_by_code('seq.cycle') or _('New')
    #     return super(Cycle, self).create(values)
class CycleLine(models.Model):
    _name = 'cycle.config.line'
    name = fields.Char()
    sequence = fields.Integer(string='Sequence', default=10)
    # number = fields.Char(
    #     default="1", compute='_compute_get_number'
    # )
    #
    # @api.depends('sequence', 'cycle_id')
    # def _compute_get_number(self):
    #     res = self.mapped('cycle_id')
    #     self.number = 0
    #     for cycle in res:
    #         number = 1
    #         for line in cycle.line_ids:
    #             line.number = number
    #             number += 1

    cycle_id = fields.Many2one(comodel_name="cycle.config", string="Cycle", required=False, )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Client Name", required=False, )
    partner_code = fields.Char(related='partner_id.partner_code',store=True)
    amount = fields.Float('Amount')
    payment_ids = fields.One2many(comodel_name="account.payment", inverse_name="cycle_line_id", string="", required=False, )
    payment_count = fields.Integer(compute='compute_payment_count')
    @api.depends('payment_ids')
    def compute_payment_count(self):
        for rec in self:
            rec.payment_count = len(rec.payment_ids)

    invoice_ids = fields.One2many(comodel_name="account.move", inverse_name="cycle_line_id", string="",
                                  required=False, )
    invoice_count = fields.Integer(compute='compute_invoice_count')

    @api.depends('invoice_ids')
    def compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = len(rec.invoice_ids)
    def action_view_payments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payments'),
            'view_mode': 'tree',
            'res_model': 'account.payment',
            'target': 'new',
            'domain':[('cycle_line_id','=',self.id)],
            'context': {
                'create': 0,
            },
        }
    def action_view_invoices(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoices'),
            'view_mode': 'tree',
            'res_model': 'account.move',
            'target': 'new',
            'domain':[('cycle_line_id','=',self.id)],
            'context': {
                'create': 0,
            },
        }