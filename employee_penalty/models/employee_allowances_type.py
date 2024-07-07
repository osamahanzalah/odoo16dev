from odoo import api, fields, models


class AllowancesType(models.Model):
    _name = 'employee.allowances.type'
    _rec_name = 'name'

    name = fields.Char()
    code = fields.Char()
