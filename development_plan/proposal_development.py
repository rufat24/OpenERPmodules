from datetime import datetime, date
from lxml import etree
import time

from openerp import SUPERUSER_ID
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

from openerp.addons.base_status.base_stage import base_stage
from openerp.addons.resource.faces import task as Task

class proposal_development(osv.osv):
    _name='proposal.development'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _columns={
        'from_whom': fields.many2one('res.users','From Whom'),
        'topic': fields.char('Topic of Suggestions', size=256),
        'sending_date': fields.date('Date of Sending '),
        'suggestion': fields.text('Suggestion'),


    }
proposal_development()
class problem_task(osv.osv):
    def wrkf_open(self, cr, uid, ids):
        self.write (cr,uid,ids, {'state':'open'} )
        return True
    def wrkf_solving(self, cr, uid, ids):
        self.write (cr,uid,ids, {'state':'solving'} )
        return True
    def wrkf_solved(self, cr, uid, ids):
        self.write (cr,uid,ids, {'state':'solved'} )
        return True

    _name='problem.task'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _columns={
        'from_whom': fields.many2one('res.users','From Whom'),
        'topic': fields.char('Topic of Suggestions', size=256),
        'sending_date': fields.date('Date of Sending '),
        'problem': fields.text('Problem'),
         'state': fields.selection([('open','Open'),('solving','Solving'),('solved','Solved')])
    }
problem_task()
class development_task(osv.osv):
    _inherit='project.task'

development_task()
class development_plan(osv.osv):
    _columns={
        'bool': fields.boolean()
    }
    _defaults ={
        'bool': False
    }
    _inherit='project.project'

