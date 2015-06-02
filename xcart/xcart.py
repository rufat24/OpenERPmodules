from openerp.osv import osv,fields
from datetime import datetime
import json
import urllib2
import psycopg2
import copy
import logging
import requests
from ConfigParser import ConfigParser
import threading
import pooler
import netsvc
import logging
import tools


class xcart_shop(osv.osv):

    _name = 'xcart.shop'
    _columns = {
        'shop_name':fields.char('Shop Name',required = True),
        'url':fields.char('Server URL',required = True),
        'key': fields.char('Key', size=256, required=True)
    }

    def import_customers(self,cr,uid,ids,context={}):
        cr.execute('select max(customer_id) customers_ids from xcart_customers')
        max_id = cr.dictfetchall()
        response = urllib2.urlopen("http://localhost/openerp_xcart/xcart_customers.php?key=1234&pmid="+str(max_id[0]['customers_ids'])).read()

        data = json.loads(response)

        i = 0
        while i < len(data):
            customer_ids = self.pool.get('xcart.customers').search(cr,uid,[('customer_id', '=',data[i]['id'])])
            if not customer_ids:
                self.pool.get('xcart.customers').create(cr,uid,{'id':data[i]['id'],'name':data[i]['firstname'],'l_name':data[i]['lastname'],'country':data[i]['country'],'city':data[i]['city'],'street':data[i]['address'],'zipcode':data[i]['zipcode'],'phone':data[i]['phone'],'registration_date':data[i]['first_login']})
            i+=1
        return True

    def import_products(self,cr,uid,ids,context={}):
        cr.execute('select max(product_id) products_ids from xcart_products')
        max_id = cr.dictfetchall()
        response = urllib2.urlopen("http://localhost/openerp_xcart/xcart_products.php?key=1234&pmid="+str(max_id[0]['products_ids'])).read()
        data = json.loads(response)

        i= 0
        while i < len(data):
            #str_descr = str(data[1]['descr']).replace("'","r\'")+

            product_ids = self.pool.get('xcart.products').search(cr,uid,[('product_id', '=',data[i]['productid'])])
            if not product_ids:
                cr.execute("insert into xcart_products (product_id, product, provider_id, list_price, category_id, manufacturer_id) values (%s,%s,%s,%s,%s,%s)",[(data[i]['productid']),(str(data[i]['product']).replace("'","r\'")),(data[i]['provider']),(data[i]['list_price']),(data[i]['categoryid']),(data[i]['manufacturerid'])])
                cr.commit()
            i+=1
        return True

    def import_providers(self,cr,uid,ids,context={}):
        cr.execute('select max(provider_id) provider_ids from xcart_providers')
        maxs_id = cr.dictfetchall()
        response = urllib2.urlopen("http://localhost/openerp_xcart/xcart_providers.php?key=1234&pmid="+str(maxs_id[0]['provider_ids'])).read()
        data = json.loads(response)
        i = 0
        while i < len(data):
            provider_ids = self.pool.get('xcart.providers').search(cr,uid,[('provider_id', '=',data[i]['id'])])
            if not provider_ids:
                self.pool.get('xcart.providers').create(cr,uid,{'provider_id':data[i]['id'],'registration_date':data[i]['first_login']})
                countryid=self.pool.get('res.country').search(cr,uid,[('code', '=',data[i]['country'])])
                idix=self.pool.get('res.partner').create(cr,uid,{'name':data[i]['company'],'provider_id':data[i]['id'],'website':data[i]['url'],'rating':data[i]['rating'],'order_count':data[i]['order_count'],'':data[i]['order_count'],'street':data[i]['address'],'city':data[i]['city'],'country_id':countryid[0],'email':data[i]['email'],'phone':data[i]['phone']})
                #self.pool.get('res.partner').create(cr,uid,{'provider_id':data[i]['id'],'name':data[i]['name'],'website':data[i]['url']})

            i+=1
            return True

    def import_catalog(self,cr,uid,ids,context):
        cr.execute('select max(catalog_id) catalogs_ids from xcart_catalogs')
        max_id = cr.dictfetchall()
        response = urllib2.urlopen("http://localhost/openerp_xcart/xcart_catalogs.php?key=1234&pmid="+str(max_id[0]['catalogs_ids'])).read()
        data = json.loads(response)
        i = 0
        while i < len(data):
            order_ids = self.pool.get('xcart.catalogs').search(cr,uid,[('catalog_id', '=',data[i]['categoryid'])])
            if not order_ids:
                self.pool.get('xcart.catalogs').create(cr,uid,{'catalog_id':data[i]['categoryid'],'catalog':data[i]['category'],'amount':data[i]['product_count']})
            i+=1
        return True

    def import_returns(self,cr,uid,ids,context):
        cr.execute('select max(returns_id) returns_id from xcart_returns')
        max_id = cr.dictfetchall()
        response = urllib2.urlopen("http://localhost/openerp_xcart/xcart_returns.php?key=1234&pmid="+str(max_id[0]['returns_id'])).read()
        data = json.loads(response)
        jesus = urllib2.urlopen("http://localhost/openerp_xcart/xcart_reasons.php?key=1234").read()
        koke = json.loads(jesus)
        koke.append('i=0')
        i = 0
        while i < len(data):
            order_ids = self.pool.get('xcart.returns').search(cr,uid,[('returns_id', '=',data[i]['returnid'])])
            self.pool.get('xcart.returns').create(cr,uid,{'returns_id':data[i]['returnid'],'returns_product':data[i]['productid'],'returns_name':data[i]['userid'],'receiver':data[i]['orderid'],'returns_date':data[i]['date'],'amount_returns':data[i]['returned_amount'],'reason':koke[int(data[i]['reason'])]})
            i+=1
        return True


    def import_orders(self,cr,uid, ids, context):
        cr.execute('select max(order_id) order_ids from xcart_orders')
        max_id = cr.dictfetchall()
        response = urllib2.urlopen("http://localhost/openerp_xcart/xcart_orders.php?key=1234&pmid="+str(max_id[0]['order_ids'])).read()
        orders_data = json.loads(response)
        i = 0
        self.import_customers(cr,uid,ids,context)
        
        while i < len(orders_data):
            order_ids = self.pool.get('xcart.orders').search(cr,uid,[('order_id', '=',orders_data[i]['orderid'])])
            if not order_ids:
                #create orders
                self.pool.get('xcart.orders').create(cr,uid,{'order_id':orders_data[i]['orderid'],'name':orders_data[i]['firstname'],'l_name':orders_data[i]['lastname'],'address':orders_data[i]['s_address'],'shipping':orders_data[i]['shipping'],'payment':orders_data[i]['subtotal'],'zipcode':orders_data[i]['s_zipcode'],'total':orders_data[i]['total'],'order_date':orders_data[i]['date']})
                #response1 = urllib2.urlopen("http://localhost/openerp_xcart/xcart_order_details.php?key=1234&oid="+orders_data[i]['orderid']).read()
                #order_details_data = json.loads(response1)
                #j = 0
                #insert data into relation table between provider, order and product
                #while j < len(order_details_data):
                 #   self.pool.get('xcart.order.details').create(cr,uid,{'xcart_provider_id':order_details_data[j]['provider'],'xcart_order_id':order_details_data[j]['orderid'],'xcart_product_id':order_details_data[j]['productid']})
                  #  j+=1
            i+=1
        #cr.execute('insert into public.test (id) values(5)')
        #cr.commit()

        #get company stores list
       # for stores in self.pool.get('company.stores').browse(cr, uid,ids, context=None):
            # get orders list for company store
            #cr.execute('select distinct xcart_order_id from xcart_order_details where xcart_provider_id='+str(stores.cprovider_id))
        #    stores_orders = self.pool.get('xcart.order.details').browse(cr,uid,ids,context=None)
         #   i=0
          #  while i <len(stores_orders):
                # get info for each order
           #     cr.execute('select * from xcart_orders where order_id='+str(stores_orders[i]['xcart_order_id']))
            #    order_info = cr.dictfetchall()
             #   j=0
              #  while j<len(order_info):
               #     sale_order_data = {
                        #'name': "SO021",
                       # 'reference': 1,
                        #'partner_id': 1,
                        #'pricelist_id': 1,
                        #'partner_invoice_id':1,
                        #'partner_shipping_id':1,
                        #'date_order': xcart_order[0]['order_date'],
                        #'shop_id' : 1,
                        #'pricelist_id':1,
                        #'company_id':121323
                    #}

                    #so_obj = self.pool.get('sale.order')
                    #soid = so_obj.create(cr, uid, sale_order_data, context=context)
                   # j+=1
               # i+=1
            #context1 = "{'xcart_provider_id': '"+str(stores.cprovider_id)+"'}"
            #for store_orders in  self.pool.get('xcart.order.details').browse(cr, uid,ids, context=context1):
                #self.sale_order_create(cr, uid, ids, context=None)
        self.action_create_so(cr, uid, ids, context=None)

        return True


    def action_create_so(self, cr, uid, ids, context=None):
        so_params = {'date':'2013-12-12', 'partner_id':1}
        pid = 1
        so_id = self.create_sale_order(cr, uid, ids, so_params, pid, context=None)
        so_line_params = {'order_id':so_id}
        self.create_sale_order_line(cr, uid, ids, so_line_params, pid, context=None)
        return True

    def create_sale_order(self, cr, uid, ids, params, partnerid, context=None):
        so_obj = self.pool.get('sale.order')
        sale_data = {
            'name': 'SOeee400110000',
            'reference': 1,
            'partner_id': partnerid,
            'pricelist_id': params['partner_id'],
            'partner_invoice_id':params['partner_id'],
            'partner_shipping_id':params['partner_id'],
            'date_order': params['date'],
            'shop_id' : 1,
            'company_id':4
        }
        so = so_obj.create(cr, uid, sale_data, context=context)
        return so

    def create_sale_order_line(self, cr, uid, ids, params, pid, context=None):
        so_line_obj = self.pool.get('sale.order.line')
        so_line_data = {
            'order_id':params['order_id'],
            'name': 'Samsung TV',
            'price_unit': 50,
            'company_id':pid,
            'salesman_id':pid,
            'state':'draft',
            'product_id':2,
            'order_partner_id':1
        }
        so = so_line_obj.create(cr, uid, so_line_data, context=context)
        return so

class xcart_products(osv.osv):
    _name = "xcart.products"
    _description = "Show json file content"

    _columns = {
        'product_id':fields.integer('Product ID'),
        'product':fields.text('Product Name',size=2048),
        'descr':fields.text('Description',size=2048),
        'provider_id':fields.integer('Provider ID'),
        'list_price':fields.float('Price'),
        'category_id': fields.integer('Category ID'),
        'manufacturer_id' : fields.integer('Manufacturer ID'),
        'order_line' : fields.one2many('xcart.order.details', 'xcart_product_id', 'Products')
        #'product_tie' : fields.many2many('xcart.orders','xcart_order_rel','product2_id','order2_id','Connection')
    }

class company_stores(osv.osv):
    _name = "company.stores"
    _columns = {
        'cprovider_id':fields.integer('Store ID'),
        'magazin_name':fields.char('Store Name',size=256)
        }

class xcart_catalogs(osv.osv):
    _name = 'xcart.catalogs'
    _rec_name='catalog'
    _rec_name='catalog'
    _columns = {
        'catalog_id' : fields.integer('Catalog ID'),
        'catalog' : fields.char('Catalog Name',size=1024, required=True),
        'amount' : fields.integer('Amount of Products for each Catalog')
    }
class xcart_returns(osv.osv):

    _name = 'xcart.returns'
    _columns = {
        'returns_id': fields.integer('Returns ID'),
        'returns_product':fields.integer('Product Name'),
        'returns_name':fields.char('Provider'),
        'receiver':fields.char('Customer'),
        'returns_date':fields.date('Returns  Date'),
        'amount_returns':fields.integer('Price of Returns'),
        'reason' : fields.text('Reasons')
    }



class xcart_orders(osv.osv):
    _name = "xcart.orders"
    _description = "Show X-Cart orders"
    _rec_name = 'address'
    _columns = {
        'order_id':fields.integer('Order Id'),
        'name': fields.char('Firstname',size=256),
        'l_name': fields.char('Lastname',size=256),
        'address':fields.char('Order Delivery Address',size=256),
        'zipcode':fields.char('Zipcode',size=256),
        'shipping':fields.char('Shipping Method',size=256),
        'payment':fields.char('Payment Method',size=256),
        'total':fields.char('Total Price',size=256),
        'order_date' : fields.date('Order Date'),
        'state':fields.selection([('queued','Queued'),('processed','Processed'),('delayed','Delayed'),('completed','Completed'),('cancelled','Cancelled')],'State',readonly="1"),
        'order_line' : fields.one2many('xcart.order.details', 'xcart_order_id', 'Orders')
    }

xcart_orders()

class xcart_customers(osv.osv):

    _name = "xcart.customers"
    _description = "Save X-Cart Customers"
    _columns = {
        'customer_id':fields.char('Customer ID',size=64),
        'name':fields.char('Name',size=256),
        'l_name':fields.char('Last Name',size=256),
        'country':fields.char('Country',size=256),
        'city':fields.char('City',size=256),
        'street':fields.char('Street',size=256),
        'zipcode':fields.char('ZIP',size=256),
        'phone':fields.char('Phone Number',size=256),
        'registration_date' : fields.datetime('Date')
    }

class xcart_providers(osv.osv):

    _name = 'xcart.providers'
    _columns = {
        'provider_id':fields.integer('Provider ID'),
        'order_line' : fields.one2many('xcart.order.details', 'xcart_provider_id', 'Providers'),
        'registration_date' : fields.datetime('Date')
    }
xcart_providers()

class xcart_res_partner(osv.osv):
    _inherit = 'res.partner'
    _columns = {
         'rating' : fields.integer('Providers Rating'),
         'order_count' : fields.integer('Order_count'),
         'provider_id': fields.integer('Provider Id')
    }

class xcart_order_details(osv.osv):
    _name = 'xcart.order.details'
    _columns = {
         'xcart_provider_id' : fields.integer('XCart Provider ID'),
         'xcart_order_id' : fields.integer('XCart Order ID'),
         'xcart_product_id' : fields.integer('XCart Product ID')
    }
xcart_res_partner()
xcart_shop()