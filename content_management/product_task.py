from datetime import datetime, date
from lxml import etree
import time

from openerp import SUPERUSER_ID
from openerp import tools
from openerp.osv import fields, osv
from openerp import netsvc
from openerp.tools.translate import _

from openerp.addons.base_status.base_stage import base_stage
from openerp.addons.resource.faces import task as Task




class product_task(osv.osv):
    def wkf_new(self, cr, uid, ids):
        self.write (cr,uid,ids, {'state':'new'} )
        return True
    def wkf_done(self, cr, uid, ids):
        self.write (cr,uid,ids, {'state':'done'} )
        return True

    _name='product.task'
    _columns={
        'responsible': fields.many2one('res.users','Responsible'),
        'deadline': fields.date('Deadline'),
        'task' :fields.text('Task'),
        'state' : fields.selection([('new','New'),('done','Done')],'State', readonly=True)
    }
class development_plan(osv.osv):
    _name='development.plan'
    _columns={
        'month': fields.date('Month'),
        'prod_id':fields.many2one('product.product','Category')
        #'category_line': fields.one2many('development.line','plan_id','Categories'),
        #'category_id': fields.related('category_line','category_id',type="many2one",relation="product.product", string="Category")
      #  'total_done': fields.function(amount_done,type=float, 'Total Done')
         #'order_line': fields.one2many('product.db.task','plan_id')
    }
development_plan()
"""
class dev_line(osv.osv):
    _name='dev.line'
    _columns={
        'category_id': fields.many2one('product.product','Category'),
        'plan_id': fields.integer('Plan ID'),
        'amount' :fields.integer('Amount of Products'),
        'responsible' : fields.many2one('res.users','Responsible'),
        'done':fields.integer('Done'),
    }
dev_line()
"""
class product_db_task(osv.osv):
    _name='product.db.task'
    _columns={
    'responsible': fields.many2one('res.users','Responsible'),
   # 'product_category' : fields.many2one('xcart.catalogs','Product Category'),
    'state' : fields.selection([('new','New'),('done','Done')]),
    'amount' :fields.integer('Amount of Products'),
    'deadline': fields.date('Deadline'),
    'done':fields.integer('Done'),
    'plan_id' : fields.many2one('development.plan','Plan'),
    'source': fields.text('Source of content'),
    'comment' : fields.integer('Comment'),
    'collection': fields.boolean('Collection'),
    'input':fields.boolean('Input')
    }
class task_page(osv.osv):
    _name='task.page'
    _columns={
        'responsible': fields.many2one('res.users','Responsible'),
        'deadline': fields.date('Deadline'),
        'page_line': fields.one2many('portal.task.page','partner_id'),
        'page_id': fields.related('page_line' ,'page_id',type="many2one",relation="portal.page")
    }
class portal_task_page(osv.osv):
   # def total_count(self, cr, uid, ids, name, arg, context=None):

    _name='portal.task.page'
    _columns={
        'page_id': fields.many2one('portal.page','List of Pages'),
        'partner_id' : fields.integer(),
        #'total':fields.function(total_count)
    }
class portal_page(osv.osv):
    _name='portal.page'
    _columns={
        'page_name': fields.char('Page Name',size=256)
    }
class plan_development(osv.osv):

    def amount_done(self, cr, uid, ids, name, args, context=None):
        res = {}
        for rec in self.browse(cr, uid, ids, context=context):
            done = 0.0
            k = 0
            for line_rec in rec.dev_line1:
                if line_rec.done>100:
                    raise osv.except_osv(_('Error!'),_('The percent value cannot be over 100%!'))
                else:
                    done += line_rec.done or 0.0
                    k+=1
            if k==0:
                done/=k+1
            else:
                done/=k

            res.update({rec.id : done})
        return res
    def button_update(self, cr, uid, ids, context=None):
        return True

    _name='plan.development'
    _columns={
        'month': fields.date('Month'),
        'catalog':fields.many2one('xcart.catalogs','Category'),
        'dev_line': fields.one2many('dev.plan.line','plan_id','Categories'),
        'category_id': fields.related('dev_line','category_id',type="many2one", relation="xcart.catalogs", string="Categories"),
        'dev_line1': fields.one2many('dev.plan.line','plan_id1','Categories'),
        'category_id1': fields.related('dev_line1','category_id1',type="many2one", relation="xcart.catalogs", string="Categories"),
        'total_done' : fields.function(amount_done,type='float', string='Total Done')
    }
plan_development()

class dev_plan_line(osv.osv):
    _name='dev.plan.line'
    _columns={
        'category_id': fields.many2one('xcart.catalogs',"Category"),
        'amount':fields.integer('Amount of Produts'),
        'responsible':fields.many2one('res.users','Responsible'),
        'done':fields.integer('Done %'),
        'plan_id' : fields.integer('Plan'),
        'plan_id1' : fields.integer('Plan')
    }
dev_plan_line()