from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    doc_types_ids = fields.Many2many(comodel_name="employee.document.type",string="Document Types", )
    no_month_expire = fields.Integer(string="Notify Expire Months",)


class ConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    doc_types_ids = fields.Many2many(related="company_id.doc_types_ids",string="Document Types",readonly=False )
    no_month_expire = fields.Integer(string="Notify Expire Months",related="company_id.no_month_expire",readonly=False)
