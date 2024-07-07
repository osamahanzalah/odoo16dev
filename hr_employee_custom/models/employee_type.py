# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployeeType(models.Model):
    _name = 'hr.employee.type'

    name = fields.Char()
