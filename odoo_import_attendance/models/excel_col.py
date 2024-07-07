# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class Att_Excel(models.Model):
    _name = 'attendance.excel.col'
    name = fields.Char(default='New')
    personal_id_col_index = fields.Integer('Personal Id Column Index',required=1)
    date_col_index = fields.Integer('Date Column Index',required=1)
    check_in_out_col_index = fields.Integer('Check In/Out Column Index',required=1)
    # ar_lang = fields.Boolean('Arabic Language')
    @api.constrains('personal_id_col_index','date_col_index','check_in_out_col_index')
    def check_position(self):
        if self.personal_id_col_index <= 0:
            raise exceptions.ValidationError("Personal Id Column Index must be greater than zero")
        if self.date_col_index <= 0:
            raise exceptions.ValidationError("Date Column Index must be greater than zero")
        if self.check_in_out_col_index <= 0:
            raise exceptions.ValidationError("Check In/Out Column Index must be greater than zero")