# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp


class Partner(models.Model):
    _inherit = 'res.partner'

    partner_code = fields.Char('Partner Code')
    partner_type = fields.Selection(string="Client Type",
                                      selection=[
                                          ('general_cycle', 'General cycle'),
                                          ('private_cycle', 'Private cycle'),
                                          ('company_cycle', 'Company cycle'),
                                                 ],
                                      required=False, )
    ambassador_name = fields.Char('Ambassador name')
    company_name = fields.Char('Company name')
    national_id = fields.Char('National ID')

    payment_method = fields.Char('Payment method')
    payback_method = fields.Char('Payback method')

