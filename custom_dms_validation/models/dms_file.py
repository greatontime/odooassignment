# Copyright 2024 Flowdoo Co., Ltd. (http://flowdoo.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models,fields,api
import logging
_logger = logging.getLogger(__name__)

class DMSFile(models.Model):
    _name = "dms.file"
    _inherit = ["dms.file", "tier.validation"]
    _state_from = ["under_approval","refuse"]
    _state_to = ["approved"]
    _check_company_auto = True
    _tier_validation_manual_config = False

    need_validation = fields.Boolean(string="Need Validation",compute="_compute_need_validation")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('under_approval', 'Under Approval'),
        ('approved', 'Approved'),
        ('refuse', 'Refused')
    ], string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True)

    def action_state_submit(self):
        for rec in self:
            if rec.state in ["draft","submit"] and not rec.directory_id.need_validation:
                rec.write({
                    "state":"submit"
                })
            elif rec.state in ["draft","submit"] and rec.directory_id.need_validation:
                rec.write({
                    "state":"under_approval"
                })
                rec.request_validation()

    def action_state_approved(self):
        for rec in self:
            if rec.state in ["draft","submit"] and not rec.directory_id.need_validation:
                rec.write({
                    "state":"approved"
                })


    def reject_tier(self):
        res = super().reject_tier()
        for review in self.review_ids:
            review.unlink()
        self.write({
            "state":"refuse"
        })
        return res
    
    def validate_tier(self):
        res = super().validate_tier()
        sequences = self._get_sequences_to_approve(self.env.user)
        reviews = self.review_ids.filtered(
            lambda l: l.sequence in sequences or l.approve_sequence_bypass
        )
        user_reviews = reviews.filtered(
            lambda r: r.status == "pending"
        )
        if not user_reviews:
            self.write({
                "state":"approved"
            })
        return res

