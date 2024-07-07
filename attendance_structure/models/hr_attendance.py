from odoo import api, fields, models
from odoo.fields import Date, Datetime


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    late = fields.Float(compute='compute_late_hours')
    early = fields.Float(compute='compute_early_hours')

    def is_public_holiday(self, resource, date):
        public_holiday = self.env['resource.calendar.leaves'].search(
            [('calendar_id', '=', resource.id), ('date_from', '<=', date),
             ('date_to', '>=', date), ('resource_id', '=', False)])
        if public_holiday:
            return True
        return False

    def is_working_day(self, resource, date):
        working_day = self.env['resource.calendar.attendance'].search(
            [('calendar_id', '=', resource.id), ('dayofweek', '=', date.weekday())],limit=1)
        if working_day:
            return working_day
        return False

    @api.depends('employee_id','check_in')
    def compute_late_hours(self):
        for rec in self:
            rec.late = 0
            if rec.check_in:
                public_holiday = rec.is_public_holiday(rec.employee_id.resource_calendar_id,rec.check_in.date())
                working_day = rec.is_working_day(rec.employee_id.resource_calendar_id,rec.check_in.date())
                if working_day and not public_holiday:
                    planned_check_in = working_day.hour_from
                    if rec.employee_id.resource_calendar_id.attendance_structure_id.flexible_hours:
                        planned_check_in += rec.employee_id.resource_calendar_id.attendance_structure_id.flexible_hours
                    check_in = Datetime.context_timestamp(rec, Datetime.from_string(rec.check_in))
                    check_in_time = check_in.time()
                    actual_check_in = check_in_time.hour + (check_in_time.minute / 60) + (
                            check_in_time.second / (60 * 60))
                    if actual_check_in < planned_check_in:
                        rec.late = 0
                    else:
                        rec.late = actual_check_in - planned_check_in

    @api.depends('employee_id', 'check_out')
    def compute_early_hours(self):
        for rec in self:
            rec.early = 0
            if rec.check_out:
                public_holiday = rec.is_public_holiday(rec.employee_id.resource_calendar_id, rec.check_out.date())
                working_day = rec.is_working_day(rec.employee_id.resource_calendar_id, rec.check_out.date())
                if working_day and not public_holiday:
                    planned_check_out = working_day.hour_to
                    check_in = Datetime.context_timestamp(rec, Datetime.from_string(rec.check_in)).time()
                    actual_check_in = check_in.hour + (check_in.minute / 60) + (
                            check_in.second / (60 * 60))
                    if actual_check_in > working_day.hour_from:
                        planned_check_out += rec.employee_id.resource_calendar_id.attendance_structure_id.flexible_hours
                    check_out = Datetime.context_timestamp(rec, Datetime.from_string(rec.check_out))
                    check_out_time = check_out.time()
                    actual_check_out = check_out_time.hour + (check_out_time.minute / 60) + (
                            check_out_time.second / (60 * 60))
                    if actual_check_out >= planned_check_out:
                        rec.early = 0
                    else:
                        rec.early = planned_check_out - actual_check_out

