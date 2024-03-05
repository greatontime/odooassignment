import binascii
import contextlib
import datetime
import hmac
import ipaddress
import itertools
import json
import logging
import os
import time
from collections import defaultdict
from hashlib import sha256
from itertools import chain, repeat
from markupsafe import Markup

import babel.core
import decorator
import pytz
from lxml import etree
from lxml.builder import E
from passlib.context import CryptContext
from psycopg2 import sql

from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command
from odoo.addons.base.models.ir_model import MODULE_UNINSTALL_FLAG
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from odoo.http import request, DEFAULT_LANG
from odoo.osv import expression
from odoo.service.db import check_super
from odoo.tools import is_html_empty, partition, collections, frozendict, lazy_property

class ResUsers(models.Model):
    _inherit = 'res.users'

    @tools.ormcache('self.id')
    def _get_company_ids(self):
        # use search() instead of `self.company_ids` to avoid extra query for `active_test`
        domain = [('active', '=', True)]
        # domain = [('active', '=', True), ('user_ids', 'in', self.id)]
        return self.env['res.company'].search(domain)._ids