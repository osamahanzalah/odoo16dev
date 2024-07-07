# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class SelectedAttendanceRecordsLines(models.Model):
    _name = 'attendance.records.lines'

    employee_id = fields.Many2one('hr.employee')
    attendance_code = fields.Char('Personnel ID',related='employee_id.attendance_code')
    check_in = fields.Datetime('Check In')
    check_out = fields.Datetime('Check Out')
    date = fields.Date('Date')
    # type = fields.Selection([('check_in','Check In'),('check_out','Check Out'),('ot_in','OT In'),('ot_out','OT Out')])