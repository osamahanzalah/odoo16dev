from odoo import api, fields, models


class PenaltyType(models.Model):
    _name = 'employee.penalty.type'
    _rec_name = 'name'

    name = fields.Char()
    code = fields.Char()
