from openerp import pooler
from openerp.osv import osv, fields
from openerp import tools
from openerp.tools.translate import _
import os
import csv

class product_load_category_wizard(osv.osv_memory):
    _name = 'product.load.category.wizard'
    _description = 'Import product categories data from .csv'

    def load_data(self, cr, uid, ids, context):
	category_obj = self.pool.get('product.category')
	archive = csv.DictReader(open('/opt/openerp/server/openerp/addons/am_migration/data/category.csv'))
	for line in archive:
	    category_id = category_obj.search(cr, uid, [('name','=',line['name'])])
	    if not category_id:
		category_obj.create(cr, uid, {'name':line['name'],'parent_id':2,'type':'normal'})
	return True

    _columns = {
        'sure': fields.boolean('Are you sure?', help="Are you sure to upload the data?"),
    }

product_load_category_wizard()
