from datetime import datetime, date
from lxml import etree
import time

from openerp import SUPERUSER_ID
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

from openerp.addons.base_status.base_stage import base_stage
from openerp.addons.resource.faces import task as Task


class provider_statistics(osv.osv):
    _inherit='xcart.providers'
    _columns={
        'month': fields.datetime('Month')
    }