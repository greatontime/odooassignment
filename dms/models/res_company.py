# Copyright 2020 Creu Blanca
# Copyright 2017-2019 MuK IT GmbH
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):

    _inherit = "res.company"

    # ----------------------------------------------------------
    # Database
    # ----------------------------------------------------------

    documents_onboarding_state = fields.Selection(
        selection=[
            ("not_done", "Not done"),
            ("just_done", "Just done"),
            ("done", "Done"),
            ("closed", "Closed"),
        ],
        default="not_done",
    )

    documents_onboarding_storage_state = fields.Selection(
        selection=[
            ("not_done", "Not done"),
            ("just_done", "Just done"),
            ("done", "Done"),
            ("closed", "Closed"),
        ],
        default="not_done",
    )

    documents_onboarding_directory_state = fields.Selection(
        selection=[
            ("not_done", "Not done"),
            ("just_done", "Just done"),
            ("done", "Done"),
            ("closed", "Closed"),
        ],
        default="not_done",
    )

    documents_onboarding_file_state = fields.Selection(
        selection=[
            ("not_done", "Not done"),
            ("just_done", "Just done"),
            ("done", "Done"),
            ("closed", "Closed"),
        ],
        default="not_done",
    )

    # ----------------------------------------------------------
    # Functions
    # ----------------------------------------------------------

    def get_and_update_onbarding_state(self, onboarding_state, steps_states):
        """ Needed to display onboarding animations only one time. """
        old_values = {}
        all_done = True
        for step_state in steps_states:
            old_values[step_state] = self[step_state]
            if self[step_state] == 'just_done':
                self[step_state] = 'done'
            all_done = all_done and self[step_state] == 'done'

        if all_done:
            if self[onboarding_state] == 'not_done':
                # string `onboarding_state` instead of variable name is not an error
                old_values['onboarding_state'] = 'just_done'
            else:
                old_values['onboarding_state'] = 'done'
            self[onboarding_state] = 'done'
        return old_values

    def get_and_update_documents_onboarding_state(self):
        return self.get_and_update_onbarding_state(
            "documents_onboarding_state", self.get_documents_steps_states_names()
        )

    def get_documents_steps_states_names(self):
        return [
            "documents_onboarding_storage_state",
            "documents_onboarding_directory_state",
            "documents_onboarding_file_state",
        ]

    # ----------------------------------------------------------
    # Actions
    # ----------------------------------------------------------

    @api.model
    def action_open_documents_onboarding_storage(self):
        return self.env.ref("dms.action_dms_storage_new").read()[0]

    @api.model
    def action_open_documents_onboarding_directory(self):
        storage = self.env["dms.storage"].search([], order="create_date desc", limit=1)
        action = self.env.ref("dms.action_dms_directory_new").read()[0]
        action["context"] = {
            **self.env.context,
            **{
                "default_is_root_directory": True,
                "default_storage_id": storage and storage.id,
            },
        }
        return action

    @api.model
    def action_open_documents_onboarding_file(self):
        directory = self.env["dms.directory"].search(
            [], order="create_date desc", limit=1
        )
        action = self.env.ref("dms.action_dms_file_new").read()[0]
        action["context"] = {
            **self.env.context,
            **{"default_directory_id": directory and directory.id},
        }
        return action

    @api.model
    def action_close_documents_onboarding(self):
        self.env.user.company_id.documents_onboarding_state = "closed"
