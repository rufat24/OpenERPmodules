import pytz
from openerp import SUPERUSER_ID
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import osv, fields
from openerp import netsvc
from openerp import pooler
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.osv.orm import browse_record, browse_null
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from openerp.osv import orm, fields
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
import re
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class advertising_campaign(osv.osv):
    def woffy_new(self, cr, uid, ids):
        self.write (cr,uid,ids, {'state':'new4'} )
        return True
    def woffy_confirm(self, cr, uid, ids):
        self.write (cr,uid,ids, {'state':'confirm4'} )
        return True
    _name = "advertising.campaign"
    _description = "Ad campaign "
    _table = "advertising_campaign"
    _rec_name= "target"
    _columns={
        'target_line':fields.one2many('target.services.line','partner_id','Targets'),
        'target_id':fields.related('target_line','target_id',type='many2one',relation='target.services', string='Targets'),
        'target':fields.char('Target of Advertising Campaign',size=256),
        'start_date':fields.date('Start Date'),
        'end_date':fields.date('End Date'),
        'budget':fields.integer('Budget'),
        'state': fields.selection([('new4','New'),('confirm4','Confirmed')])
    }
    _defaults = {
        'state': 'new4'
    }

advertising_campaign()

class target_services(osv.osv):
    _name="target.services"
    _description="This class contains all targets "
    _columns={
        'name':fields.char('Target', required=True),
        'desc':fields.text('Description')
    }
    _defaults = {
    }
target_services()

class target_services_line(osv.osv):
    _name="target.services.line"
    _description="This class relates Targets"
    _columns={
        'target_id':fields.many2one('target.services','Target'),
        'values':fields.integer('Values'),
        'actual_values':fields.integer('Actual Values',  readonly=True,),
        'partner_id':fields.integer('Partner')
    }
    _defaults = {
    }
target_services_line()

class plan_campaign(osv.osv):
    _name="plan.campaign"
    _description="Plan Campaign "
    _columns={
        'ad_campaign':fields.many2one('advertising.campaign','Advertising Campaign'),
        'action_line':fields.one2many('action.plan.line','partner_id','Plan'),
        'action_id':fields.related('action_line','action_id',type='many2one',relation='action.services', string='Targets'),
    }
    _defaults = {
    }



plan_campaign()

class action_services(osv.osv):
    _name="action.services"
    _description="Action"
    _columns={
        'name':fields.char('Target'),
        'desc':fields.text('Description')
    }
    _defaults = {
    }
action_services()


class action_services_line(osv.osv):
    _name="action.plan.line"
    _description="Action Plan"
    _columns={
        'action_id':fields.many2one('action.services','Target'),
        'channel':fields.integer('Channel'),
        'cost':fields.integer('Cost'),
        'partner_id':fields.integer('Partner')
    }
    _defaults = {
    }

action_services_line()

class campaign_result(osv.osv):
    _inherit = 'plan.campaign'

campaign_result()

class optimization_plan(osv.osv):
    def wkf_new(self, cr, uid, ids):
        self.write (cr,uid,ids, {'state':'new'} )
        return True
    def wkf_confirm(self, cr, uid, ids):
        self.write (cr,uid,ids, {'state':'confirm'} )
        return True
    def wkf_done(self, cr, uid, ids):
        self.write (cr,uid,ids, {'state':'done'} )
        return True

    _name= 'optimization.plan'
    _columns={
        'responsible': fields.many2one('res.users','Responsible'),
        'start_date': fields.date('Start Date'),
        'finish_date': fields.date('Finish Date'),
        'link_list': fields.text('A List of Links and Sections to Optimization'),
        'keywords': fields.text('Keywords'),
        'external_links': fields.text('External Links'),
        'state': fields.selection([('new','New'),('confirm','Confirm'),('done','Done')],'State', readonly=True)
    }
    _defaults={
        'state': 'new'
    }
optimization_plan()


class copywriting_plan(osv.osv):
    def wrkf_new(self, cr, uid, ids):
        self.write (cr,uid,ids, {'state':'new1'} )
        return True
    def wrkf_confirm(self, cr, uid, ids):
        self.write (cr,uid,ids, {'state':'confirm1'} )
        return True
    def wrkf_done(self, cr, uid, ids):
        self.write (cr,uid,ids, {'state':'done1'} )
        return True

    _name= 'copywriting.plan'
    _columns={
        'copywriter': fields.many2one('res.users','Copywriter'),
        'start_date': fields.date('Start Date'),
        'finish_date': fields.date('Finish Date'),
        'keywords_list': fields.text('List of Keywords'),
        'optimization_request': fields.text('Request for Optimization'),
        'type': fields.selection([('analytical articles','Analytical articles'),('scientific articles','Scientific articles'),('news articles','News articles'),('news','News'),('advertorials','Advertorials'),('imaginative literature','Imaginative literature')],'Type of the Articles'),
        'title': fields.char('Title of the Articles',size=256),
        'percent': fields.integer('The Percentage of the Keywords'),
        'state': fields.selection([('new1','New'),('confirm1','Confirm'),('done1','Done')],'State', readonly=True)
    }
    _defaults={
        'state': 'new1'
    }

class optimization_part(osv.osv):
    def wrkfl_new(self, cr, uid, ids):
        self.write (cr,uid,ids, {'state':'new2'} )
        return True
    def wrkfl_confirm(self, cr, uid, ids):
        self.write (cr,uid,ids, {'state':'confirm2'} )
        return True
    def wrkfl_done(self, cr, uid, ids):
        self.write (cr,uid,ids, {'state':'done2'} )
        return True

    _name= 'optimization.part'
    _columns={
        'responsible': fields.many2one('res.users','Responsible'),
        'start_date': fields.date('Start Date'),
        'finish_date': fields.date('Finish Date'),
        'opt_descr': fields.boolean('Optimization of Meta Descriptions'),
        'opt_site': fields.boolean('Optimization Maps of Site'),
        'opt_tags': fields.boolean('Optimization of Meta Tags'),
        'state': fields.selection([('new2','New'),('confirm2','Confirm'),('done2','Done')],'State', readonly=True)
    }
    _defaults={
        'state': 'new2'
    }
class marketing_campaign_workitem(osv.osv):
    _inherit='marketing.campaign.workitem'
class marketing_campaign_segment(osv.osv):
    _inherit='marketing.campaign.segment'
class marketing_campaign(osv.osv):
    _inherit= 'marketing.campaign'
class  marketing_campaign_transition(osv.osv):
    _inherit='marketing.campaign.transition'



