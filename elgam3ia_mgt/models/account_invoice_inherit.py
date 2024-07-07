# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class AccountMove(models.Model):
    _inherit = "account.move"
    cycle_line_id = fields.Many2one('cycle.config.line', string='Cycle Member Line')
    cycle_id = fields.Many2one('cycle.config', string='Cycle', related='cycle_line_id.cycle_id', store=True)
    partner_code = fields.Char('Partner Code')
    invoice_code = fields.Char('Invoice Code')
    cycle_code = fields.Char('Cycle ID', store=True)
