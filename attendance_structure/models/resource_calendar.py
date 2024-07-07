from odoo import api, fields, models


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    attendance_structure_id = fields.Many2one(comodel_name="attendance.structure", string="",)