from odoo import api, fields, models


class AttendanceStructure(models.Model):
    _name = 'attendance.structure'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char()
    flexible_hours = fields.Float(string="",  required=False, )
    structure_ids = fields.Many2many(comodel_name="attendance.deduction.rules",)
