from openerp import pooler
from openerp.osv import osv, fields
from openerp import tools
from openerp.tools.translate import _
import os
import csv
import re
import math

class product_migration_wizard(osv.osv_memory):
    _name = 'product.migration.wizard'
    _description = 'Import product data from .csv'

    def create_product_group(self, cr, uid, ids, product_name, context):
        attribute = self.pool.get('product.attribute')
        attribute_id = attribute.search(cr, uid, [('name','=',product_name)]) and \
                        attribute.search(cr, uid, [('name','=',product_name)])[0] or \
                        attribute.create(cr, uid, {'name': product_name})
        return attribute_id

    def get_one2many(self, cr, uid, ids, line_value, model_obj, context):
        one2many_ids = []
        if "," in line_value:
            for split in line_value.split(','):
                search_id = model_obj.search(cr, uid, [('name','=',split.strip(' '))])
                if search_id:
                    one2many_ids.append(search_id[0])
        else:
            search_id = model_obj.search(cr, uid, [('name','=',line_value)])
            if search_id:
                one2many_ids.append(search_id[0])
        return one2many_ids

    def import_data(self, cr, uid, ids, context):
	archive = csv.DictReader(open("/opt/openerp/server/openerp/addons/am_migration/data/product_demo_shoes_v8.csv"))
        #~ archive = csv.DictReader(open("/home/openerp/instancias/7.0/milani/am_migration/data/product_demo_shoes_v8.csv"))
        colors = {
                'WHITE': 'WHT',
                'BLACK': 'BLK',
                'YELLOW': 'YEL',
                'ORANGE': 'ORG',
                'FUXIA': 'FUX',
                'RED': 'RED',
                'WHITE LEATHER': 'WHT LEATHER',
                'SILVER': 'SLV',
                'GREEN': 'GRN',
                'BLACK LEATHER': 'BLK LEATHER',
                'BLACK - SILVER DET.': 'BLK SLV',
                'BLACK - WHITE DET.': 'BLK WHT',
                'CELESTE': 'CEL',
                'GREY': 'GRY',
                'BLUE': 'BLU',
        }
        sizes = ['37','38','39','40','41','42','43','44','45','46','47','48']
        currency_obj = self.pool.get('res.currency')
	category_obj = self.pool.get('product.category')
	manufacturer_obj = self.pool.get('manufacturer.master')
	activity_obj = self.pool.get('activity.master')
	barbore_obj = self.pool.get('bar.bore.diameter.master')
	brakes_obj = self.pool.get('brakes.master')
	brand_obj = self.pool.get('partner.brand')
	color_obj = self.pool.get('color.master')
	design_obj = self.pool.get('design.master')
	gender_obj = self.pool.get('gender.master')
	htube_obj = self.pool.get('head.tube.master')
	rake_obj = self.pool.get('rake.master')
	seat_obj = self.pool.get('seat.post.diameter.master')
	size_obj = self.pool.get('size.master')
	specialty_obj = self.pool.get('specialty.master')
	taxle_obj = self.pool.get('taxle.master')
	ussize_obj = self.pool.get('ussize.master')
	wheel_obj = self.pool.get('wheel.size.master')
	width_obj = self.pool.get('width.master')
	oo_obj = self.pool.get('width.oo.master')
	finish_obj = self.pool.get('finish.master')
	release_obj = self.pool.get('release.master')
	bbraket_obj = self.pool.get('bottom.braket.master')
	product_obj = self.pool.get('product.product')
        sql = cr.execute(''' select  MAX(default_code) FROM product_product ''')
        sql = cr.fetchone()
        product_code = int(sql[0]) + 1
	for line in archive:
            for size in sizes:
                color = line['color_id'].strip() in colors and colors[line['color_id'].strip()] or ''
                activity_ids = self.get_one2many(cr, uid, ids, line['activity_id'], activity_obj, context)
                finish_ids = self.get_one2many(cr, uid, ids, line['finish'], finish_obj, context)
                gender_ids = self.get_one2many(cr, uid, ids, line['Gender'], gender_obj, context)
                currency_id = currency_obj.search(cr, uid, [('name','=',line['currency'])])
                cur_brw = currency_obj.browse(cr, uid, currency_id[0], context)
                category_id = category_obj.search(cr, uid, [('name','=',line['category_id'])])
                manufacturer_id = manufacturer_obj.search(cr, uid, [('code','=',line['manufacturer_id'])])
                barbore_id = barbore_obj.search(cr, uid, [('name','=',line['bar_bore_diameter_id'])])
                brake_id = brakes_obj.search(cr, uid, [('name','=',line['brakes_id'])])
                brand_id = brand_obj.search(cr, uid, [('name','=',line['brand_name'])])
                color_id = color_obj.search(cr, uid, [('name','=',color)])
                design_id = design_obj.search(cr, uid, [('name','=',line['design_id'])])
                htube_id = htube_obj.search(cr, uid, [('name','=',line['head_tube_id'])])
                rake_id = rake_obj.search(cr, uid, [('name','=',line['rake_id'])])
                seat_id = seat_obj.search(cr, uid, [('name','=',line['seat_post_diameter_id'])])
                #~ size_id = size_obj.search(cr, uid, [('name','=',line['size_id'])])
                size_id = size_obj.search(cr, uid, [('name','=',size)])
                specialty_id = specialty_obj.search(cr, uid, [('name','=',line['specialty_id'])])
                taxle_id = taxle_obj.search(cr, uid, [('name','=',line['taxle_id'])])
                ussize_id = ussize_obj.search(cr, uid, [('name','=',line['ussize_id'])])
                wheel_id = wheel_obj.search(cr, uid, [('name','=',line['wheel_size_id'])])
                width_id = width_obj.search(cr, uid, [('name','=',line['width_id'])])
                oo_id = oo_obj.search(cr, uid, [('name','=',line['width_oo_id'])])
                release_id = release_obj.search(cr, uid, [('name','=',line['release'])])
                bbraket_id = bbraket_obj.search(cr, uid, [('name','=',line['bottom_braket'])])
                #~ product_id = product_obj.search(cr, uid, [('default_code','=',line['internal_ref_id'])])
                product_id = product_obj.search(cr, uid, [('default_code','=',product_code)])
                if not product_id:
                    p = product_obj.create(cr, uid, {
			'name': line['product_name'],
			'categ_id': category_id and category_id[0] or '',
                        'attribute_id': self.create_product_group(cr, uid, ids, line['product_name'].strip(), context),
			'sale_ok': True,
			'purchase_ok': True,
			#~ 'default_code': line['internal_ref_id'],
			'default_code': str(product_code),
			'type': 'product',
			'standard_price': line.get('cost_price') and float(line['cost_price'])/cur_brw.rate_silent or 0.00,
			'list_price': line.get('retail_price_net') and float(line['retail_price_net'])/cur_brw.rate_silent or 0.00,
			'description': line['description'],
			'procure_method': 'make_to_stock',
			'supply_method': 'buy',
			#~ 'x_factor': line['x_factor'],
			'sport': line['sport'],
			'spcl_tech': line['SpecialTechnology'],
			'material_desc': line['MaterialDesc'],
			'material': line['material'],
			'color_id': color_id and color_id[0] or color_obj.create(cr, uid, {'name':color}),
			'design_id': design_id and design_id[0] or '',
			'bar_id': barbore_id and barbore_id[0] or '',
			'rake_id': rake_id and rake_id[0] or '',
			'width_oo_id': oo_id and oo_id[0] or '',
			'activity_id': [(6,0,activity_ids)],
			'specialty_id': specialty_id and specialty_id[0] or '',
			'brand_id': brand_id and brand_id[0] or '',
			'wheel_size_id': wheel_id and wheel_id[0] or '',
			'size_id': size_id and size_id[0] or '',
			'taxle_id': taxle_id and taxle_id[0] or '',
			'brakes_id': brake_id and brake_id[0] or '',
			'head_tube_id': htube_id and htube_id[0] or '',
			'width_id': width_id and width_id[0] or '',
			'ussize_id': ussize_id and ussize_id[0] or '',
			'manufacturer_id': manufacturer_id and manufacturer_id[0] or '',
			'release': release_id and release_id[0] or '',
			'bottom_braket': bbraket_id and bbraket_id[0] or '',
			'finish': [(6,0,finish_ids)],
			'gender_id': [(6,0,gender_ids)],
                        })
                    print 'product [%s] is been created '%product_obj.read(cr, uid, [p], ['default_code'], context)
                    product_code = product_code + 1
	return True

    _columns = {
        'sure': fields.boolean('Are you sure?', help="Are you sure to upload the data?"),
    }
product_migration_wizard()
