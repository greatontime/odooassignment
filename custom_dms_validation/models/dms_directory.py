from odoo import models,fields,api

class DmsDirectory(models.Model):
    _inherit = "dms.directory"

    need_validation= fields.Boolean("Need Validation")