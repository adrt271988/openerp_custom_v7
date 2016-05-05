from openerp import pooler
from openerp.osv import osv, fields
from openerp import tools
from openerp.tools.translate import _
import os
import csv

class product_load_masters_wizard(osv.osv_memory):
    _name = 'product.load.masters.wizard'
    _description = 'Import masters data from .csv'

    def load_data(self, cr, uid, ids, context):
	paths = {
		    'activity.master': '/opt/openerp/server/openerp/addons/am_migration/data/activity.csv',
		    'bar.bore.diameter.master': '/opt/openerp/server/openerp/addons/am_migration/data/bar_bore.csv',
		    'brakes.master': '/opt/openerp/server/openerp/addons/am_migration/data/brakes.csv',
		    'partner.brand': '/opt/openerp/server/openerp/addons/am_migration/data/brand.csv',
		    'color.master': '/opt/openerp/server/openerp/addons/am_migration/data/color.csv',
		    'design.master': '/opt/openerp/server/openerp/addons/am_migration/data/design.csv',
		    'gender.master': '/opt/openerp/server/openerp/addons/am_migration/data/gender.csv',
		    'head.tube.master': '/opt/openerp/server/openerp/addons/am_migration/data/head_tube.csv',
		    'manufacturer.master': '/opt/openerp/server/openerp/addons/am_migration/data/manufacturer.csv',
		    'rake.master': '/opt/openerp/server/openerp/addons/am_migration/data/rake.csv',
		    'seat.post.diameter.master': '/opt/openerp/server/openerp/addons/am_migration/data/seat_post.csv',
		    'size.master': '/opt/openerp/server/openerp/addons/am_migration/data/size.csv',
		    'specialty.master': '/opt/openerp/server/openerp/addons/am_migration/data/specialty.csv',
		    'taxle.master': '/opt/openerp/server/openerp/addons/am_migration/data/t-axle.csv',
		    'ussize.master': '/opt/openerp/server/openerp/addons/am_migration/data/ussize.csv',
		    'wheel.size.master': '/opt/openerp/server/openerp/addons/am_migration/data/wheel.csv',
		    'width.master': '/opt/openerp/server/openerp/addons/am_migration/data/width.csv',
		    'width.oo.master': '/opt/openerp/server/openerp/addons/am_migration/data/width_oo.csv',
		    'bottom.braket.master': '/opt/openerp/server/openerp/addons/am_migration/data/bottom_braket.csv',
		    'finish.master': '/opt/openerp/server/openerp/addons/am_migration/data/finish.csv',
		    'release.master': '/opt/openerp/server/openerp/addons/am_migration/data/release.csv',
		}
	category_obj = self.pool.get('product.category')
	for path in paths:
	    archive = csv.DictReader(open(paths[path]))
	    for line in archive:
		obj_id = self.pool.get(path).search(cr, uid, [('name','=',line['name'])])
		if 'category_id' in line:
		    category_id = category_obj.search(cr, uid, [('name','=',line['category_id'])])
		    if not obj_id:
			self.pool.get(path).create(cr, uid, {'name':line['name'],'category_id':category_id and category_id[0] or ''})
		elif 'code' in line:
		    if not obj_id:
			self.pool.get(path).create(cr, uid, {'name':line['name'],'code':line['code']})
		else:
		    if not obj_id:
			self.pool.get(path).create(cr, uid, {'name':line['name']})
	return True

    _columns = {
        'sure': fields.boolean('Are you sure?', help="Are you sure to upload the data?"),
    }

product_load_masters_wizard()
