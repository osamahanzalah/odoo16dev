from odoo import api, fields, models
import pandas as pd


class PayslipAttendance(models.Model):
    _name = 'hr.payslip.attendance'
    _rec_name = 'name'

    name = fields.Char(string="Description")
    employee_id = fields.Many2one(comodel_name="hr.employee", )
    date = fields.Date(string="Day")
    check_in = fields.Datetime()
    check_out = fields.Datetime()
    hours = fields.Float()
    applied_hours = fields.Float()
    payslip_id = fields.Many2one(comodel_name="hr.payslip")


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    deduction_ids = fields.One2many(comodel_name="hr.payslip.attendance", inverse_name="payslip_id")
    absent_amount = fields.Float(compute='compute_absent_deduction_amount', store=True)
    late_amount = fields.Float(compute='compute_late_deduction_amount', store=True)
    early_amount = fields.Float(compute='compute_early_deduction_amount', store=True)

    def is_public_holiday(self, resource, date):
        public_holiday = self.env['resource.calendar.leaves'].search(
            [('calendar_id', '=', resource.id), ('date_from', '<=', date),
             ('date_to', '>=', date), ('resource_id', '=', False)])
        if public_holiday:
            return True
        return False

    def is_working_day(self, resource, date):
        working_day = self.env['resource.calendar.attendance'].search(
            [('calendar_id', '=', resource.id), ('dayofweek', '=', date.weekday())], limit=1)
        if working_day:
            return working_day
        return False

    def check_has_leave(self, day):
        leave = self.env['hr.leave'].search(
            [('employee_id', '=', self.employee_id.id), ('date_from', '>=', day), ('date_to', '<=', day),
             ('state', '=', 'validate')])
        if leave:
            return True
        return False

    def get_employee_attendance(self):
        attendance_list = self.env['hr.attendance'].search(
            [('employee_id', '=', self.employee_id.id), ('check_in', '>=', self.date_from),
             ('check_out', '<=', self.date_to)])
        return attendance_list

    @api.depends('deduction_ids', 'deduction_ids.applied_hours', 'deduction_ids.name')
    def compute_absent_deduction_amount(self):
        for rec in self:
            rec.absent_amount = sum(rec.deduction_ids.filtered(lambda x: x.name == 'Absent').mapped('applied_hours')) * \
                                rec.employee_id.contract_id.hour_value

    @api.depends('deduction_ids', 'deduction_ids.applied_hours', 'deduction_ids.name')
    def compute_late_deduction_amount(self):
        for rec in self:
            rec.late_amount = sum(rec.deduction_ids.filtered(lambda x: x.name == 'Late').mapped('applied_hours')) * \
                              rec.employee_id.contract_id.hour_value

    @api.depends('deduction_ids', 'deduction_ids.applied_hours', 'deduction_ids.name')
    def compute_early_deduction_amount(self):
        for rec in self:
            rec.early_amount = sum(rec.deduction_ids.filtered(lambda x: x.name == 'Early Checkout').mapped('applied_hours')) * \
                               rec.employee_id.contract_id.hour_value

    def get_absent_deduction(self):
        for rec in self:
            rules = []
            resource_id = rec.employee_id.resource_calendar_id
            absent_rule = resource_id.attendance_structure_id.structure_ids.filtered(
                lambda x: x.duration_type == 'absent')
            if not absent_rule:
                continue
            repetition = 0
            attendance_list = [line.date() for line in rec.get_employee_attendance().mapped('check_in')]
            for single_day in pd.date_range(self.date_from, self.date_to):
                working_day = rec.is_working_day(rec.employee_id.resource_calendar_id, single_day)
                public_holiday = rec.is_public_holiday(rec.employee_id.resource_calendar_id, single_day)
                has_leave = rec.check_has_leave(single_day)
                if working_day and not public_holiday and not has_leave:
                    if single_day not in attendance_list:
                        repetition += 1
                        penalty = absent_rule[0].get_penalty(repetition, resource_id.hours_per_day)
                        rules.append((0, 0, {'payslip_id': rec.id,
                                             'employee_id': rec.employee_id.id,
                                             'hours': resource_id.hours_per_day,
                                             'applied_hours': penalty,
                                             'name': 'Absent',
                                             'date': single_day
                                             }))
            rec.write({'deduction_ids': rules})

    def get_late_rule(self, attendance_structure_id, late_time):
        late_rules = attendance_structure_id.structure_ids.filtered(lambda x: x.duration_type == 'late')
        for rule in late_rules:
            if rule.remaining:
                return rule
            elif rule.from_time <= late_time <= rule.to_time:
                return rule

    def get_late_deduction(self):
        rule_repetition = {}
        for rec in self:
            rules = []
            resource_id = rec.employee_id.resource_calendar_id
            attendance_list = rec.get_employee_attendance().sorted(key='check_in')
            for single_day in attendance_list:
                if single_day.late > 0:
                    late_rule = rec.get_late_rule(resource_id.attendance_structure_id, single_day.late)
                    if late_rule:
                        if rule_repetition.get(late_rule):
                            rule_repetition[late_rule] += 1
                        else:
                            rule_repetition[late_rule] = 1
                        penalty = late_rule[0].get_penalty(rule_repetition[late_rule], resource_id.hours_per_day,
                                                           single_day.late)
                        rules.append((0, 0, {'payslip_id': rec.id,
                                             'employee_id': rec.employee_id.id,
                                             'hours': single_day.late,
                                             'applied_hours': penalty,
                                             'name': 'Late',
                                             'date': single_day.check_in,
                                             'check_in': single_day.check_in,
                                             'check_out': single_day.check_out
                                             }))
            rec.write({'deduction_ids': rules})

    def get_early_rule(self, attendance_structure_id, late_time):
        late_rules = attendance_structure_id.structure_ids.filtered(lambda x: x.duration_type == 'early')
        for rule in late_rules:
            if rule.remaining:
                return rule
            elif rule.from_time <= late_time <= rule.to_time:
                return rule

    def get_early_deduction(self):
        rule_repetition = {}
        for rec in self:
            rules = []
            resource_id = rec.employee_id.resource_calendar_id
            attendance_list = rec.get_employee_attendance().sorted(key='check_in')
            for single_day in attendance_list:
                if single_day.early > 0:
                    early_rule = rec.get_early_rule(resource_id.attendance_structure_id, single_day.early)
                    if early_rule:
                        if rule_repetition.get(early_rule):
                            rule_repetition[early_rule] += 1
                        else:
                            rule_repetition[early_rule] = 1
                        penalty = early_rule[0].get_penalty(rule_repetition[early_rule], resource_id.hours_per_day,
                                                            single_day.early)
                        rules.append((0, 0, {'payslip_id': rec.id,
                                             'employee_id': rec.employee_id.id,
                                             'hours': single_day.late,
                                             'applied_hours': penalty,
                                             'name': 'Early Checkout',
                                             'date': single_day.check_in,
                                             'check_in': single_day.check_in,
                                             'check_out': single_day.check_out
                                             }))
            rec.write({'deduction_ids': rules})

    def compute_sheet(self):
        self.deduction_ids.unlink()
        self.get_absent_deduction()
        self.get_late_deduction()
        self.get_early_deduction()
        return super(HrPayslip, self).compute_sheet()
