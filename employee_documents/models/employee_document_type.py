# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmployeeDocumentType(models.Model):
    _name = 'employee.document.type'
    _description = "Documents Types"

    name = fields.Char(string='Document Name', copy=False, required=1)
    code = fields.Char(string='Code', copy=False)



