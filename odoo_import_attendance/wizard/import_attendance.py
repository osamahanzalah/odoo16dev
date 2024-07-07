# -*- coding: utf-8 -*-
import tempfile
import binascii
import xlrd
import logging
from datetime import datetime, date, timedelta
from odoo.exceptions import Warning, ValidationError
from odoo import models, fields, api, _
from pytz import timezone, utc

_logger = logging.getLogger(__name__)

try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    from io import StringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class ImportAttendance(models.TransientModel):
    _name = "import.attendance"

    file = fields.Binary(string='Import XLS File')
    filename = fields.Char()
    lines = fields.Many2many(comodel_name="attendance.records.lines", string="", )
    def create_attendance(self):

        attendances = self.env['hr.attendance']
        for line in self.lines:
            if line.check_in:
                emp_attendance = self.env['hr.attendance'].search([
                    ('employee_id', '=', line.employee_id.id),
                    ('date', '=', line.date)
                ], limit=1)

                if not emp_attendance:
                    values = {
                        'employee_id': line.employee_id.id,
                        'date': line.date,
                        'check_in': line.check_in,
                        'check_out': line.check_out,
                    }
                    attendances.with_context(esc = 1).create(values)
                else:
                    if emp_attendance.check_in > line.check_in:
                        emp_attendance.check_in  = line.check_in
                    if line.check_out:
                        if emp_attendance.check_out and emp_attendance.check_out < line.check_out:
                            emp_attendance.check_out = line.check_out
                        elif not emp_attendance.check_out:
                            emp_attendance.check_out = line.check_out

        if self.lines:
            self.env['attendance.records.lines'].search([]).unlink()
            res = self.env.ref("hr_attendance.hr_attendance_action")
            action = res.read()[0]
            return action
    def import_attendance(self):
        if not self.file:
            raise ValidationError(_("There is no file"))
        else:
            tmp = self.filename.split('.')
            ext = tmp[len(tmp) - 1]
            if ext not in ['xls','xlsx']:
                raise ValidationError(_("The file must be a Xls file"))
        record_lines = self.env['attendance.records.lines']
        self.env['attendance.records.lines'].search([]).unlink()
        fx = tempfile.NamedTemporaryFile(suffix=".xlsx")
        fx.write(binascii.a2b_base64(self.file))
        fx.seek(0)
        workbook = xlrd.open_workbook(fx.name)
        sheet = workbook.sheet_by_index(0)
        date_time_format = "%Y-%m-%d %H:%M:%S"
        excel_col_obj = self.env['attendance.excel.col'].search([],limit=1)
        if not excel_col_obj:
            raise ValidationError("Please Define Excel Columns under Attendances/Manage Attendances/excel columns menu")
        for row_no in range(sheet.nrows):
            if row_no <= 0:
                field = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
                labels = list(map(lambda row: str(row.value), sheet.row(row_no)))
                # if 'Date And Time' not in labels:
                #     raise ValidationError("First Column [Date And Time] not exist in this file")
                # if 'Personnel ID' not in labels:
                #     raise ValidationError("Second Column [Personnel ID] not exist in this file")
                # if 'In/Out Status' not in labels:
                #     raise ValidationError("Seven Column [In/Out Status] not exist in this file")
            else:
                attendance_line = list(map(lambda row: str(row.value), sheet.row(row_no)))
                check_date_time = datetime.strptime(str(attendance_line[excel_col_obj.date_col_index-1]), date_time_format)
                check_date_time = timezone(self.env.context['tz']).localize(
                    fields.Datetime.from_string(check_date_time), is_dst=None).astimezone(utc)

                check_date = check_date_time.date()
                check_date_time = datetime.strptime(str(check_date_time)[0:19], "%Y-%m-%d %H:%M:%S")

                emp = self.env['hr.employee'].search([('attendance_code', '=', attendance_line[excel_col_obj.personal_id_col_index-1])])
                if emp:
                    values = {
                        'employee_id': emp.id,
                        'date': check_date,
                        'check_in': check_date_time if attendance_line[excel_col_obj.check_in_out_col_index-1] in ['Check-In', 'حضور'] else False,
                        'check_out': check_date_time if attendance_line[excel_col_obj.check_in_out_col_index-1] in ['Check-Out', 'إنصراف'] else False,
                    }
                    if attendance_line[8] in ['Check-In', 'حضور']:
                        record = self.env['attendance.records.lines'].search([('date', '=', check_date),('employee_id','=', emp.id),],limit=1)
                        if record:
                            if record.check_in:
                                if record.check_in > check_date_time:
                                    record.check_in = check_date_time
                                else:
                                    continue
                            else:
                                record.check_in = check_date_time
                        else:
                            record_lines |= self.env['attendance.records.lines'].create(values)
                    elif attendance_line[excel_col_obj.check_in_out_col_index-1] in ['Check-Out', 'إنصراف']:
                        record = self.env['attendance.records.lines'].search(
                            [('date', '=', check_date),('employee_id', '=', emp.id), ], limit=1)
                        if record:
                            if record.check_out:
                                if record.check_out < check_date_time:
                                    record.check_out = check_date_time
                                else:
                                    continue
                            else:
                                record.check_out = check_date_time
                        else:
                            record_lines |=self.env['attendance.records.lines'].create(values)

        self.lines = record_lines.ids
        res = self.env.ref("odoo_import_attendance.action_attendance")
        action = res.read()[0]
        action['res_id'] = self.id
        return action
