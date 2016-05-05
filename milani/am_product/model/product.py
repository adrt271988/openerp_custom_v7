# -*- encoding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import decimal_precision as dp
import pooler
import time
import math

class finish_master(osv.osv):
    '''Finish Master'''
    _name = 'finish.master'
    
    _columns = {
        'name': fields.char('Name',help="Finish"),
    }

finish_master()

class bottom_braket_master(osv.osv):
    '''Bottom Braket Master'''
    _name = 'bottom.braket.master'
    
    _columns = {
        'name': fields.char('Name',help="Bottom Braket Name"),
        'category_id': fields.many2one('product.category','Category'),
    }

bottom_braket_master()

class release_master(osv.osv):
    '''Release Master'''
    _name = 'release.master'
    
    _columns = {
        'name': fields.char('Name',help="Release Name"),
    }

release_master()

class inherited_manufacturer(osv.osv):
    '''Manufacturer Inheritence '''
    _inherit = 'manufacturer.master'
    
    _columns = {
        'code': fields.char('Manufacturer Code', size=7,help="Manufacturer Code"),
    }

inherited_manufacturer()

class inherited_product(osv.osv):
    
    '''Product Inheritence '''
    
    _inherit = 'product.product'

    def _get_default_code(self, cr, uid, context=None):
        cr.execute(''' SELECT MAX(default_code) AS max_code FROM product_product ''')
	res = cr.dictfetchall()
	if res:
	    return str(int(res[0]['max_code']) + 1)
	else:
	    return '101000'

    def _calculate_list_price(self, cr, uid, ids, name, arg, context):
        res = dict.fromkeys(ids, 0)
        product = self.browse(cr, uid, ids[0], context = context)
	res[ids[0]] = float(product.standard_price * product.x_factor)
        return res
	
    def _calculate_xfactor(self, cr, uid, ids, name, arg, context):
        res = dict.fromkeys(ids, 0)
        product = self.browse(cr, uid, ids[0], context = context)
	res[ids[0]] = product.standard_price != 0.00 and float(product.list_price / product.standard_price) or 0.00
        return res
	
    def _calculate_avg_cost(self, cr, uid, ids, name, arg, context):
        res = dict.fromkeys(ids, 0)
	average = self.pool.get('am.average.cost')
	average_ids = average.search(cr, uid, [('product_id','=',ids[0])])
	if average_ids:
	    total_qty = 0
	    total_landed = 0
	    for avg_brw in average.browse(cr, uid, average_ids):
		total_qty += avg_brw.quantity
		total_landed += avg_brw.landed_cost + (avg_brw.standard_cost*avg_brw.quantity)
	    res[ids[0]] = float(total_landed/total_qty)
        return res

    def get_description_name(self, cr, uid, ids, name, arg, context):
	res = dict.fromkeys(ids, 0)
	vals = self.read(cr, uid, ids, [])[0]
	barbore = vals.get('bar_id') and vals['bar_id'][1]+' ' or ''
	brake = vals.get('brakes_id') and vals['brakes_id'][1]+' ' or ''
	brand = vals.get('brand_id') and vals['brand_id'][1]+' ' or ''
	color = vals.get('color_id') and vals['color_id'][1]+' ' or ''
	design = vals.get('design_id') and vals['design_id'][1]+' ' or ''
	htube = vals.get('head_tube_id') and vals['head_tube_id'][1]+' ' or ''
	rake = vals.get('rake_id') and vals['rake_id'][1]+' ' or ''
	seat = vals.get('seat_id') and vals['seat_id'][1]+' ' or ''
	size = vals.get('size_id') and vals['size_id'][1]+' ' or ''
	taxle = vals.get('taxle_id') and vals['taxle_id'][1]+' ' or ''
	ussize = vals.get('ussize_id') and vals['ussize_id'][1]+' ' or ''
	wheel = vals.get('wheel_size_id') and vals['wheel_size_id'][1]+' ' or ''
	width = vals.get('width_id') and vals['width_id'][1]+' ' or ''
	oo = vals.get('width_oo_id') and vals['width_oo_id'][1]+' ' or ''
	material = vals.get('material') and vals['material']+' ' or ''
	material_desc = vals.get('material_desc') and vals['material_desc']+' ' or ''
	res[ids[0]] = vals.get('type') == 'product' and \
			size+width+wheel+htube+brake+taxle+rake+oo+seat+barbore+design+color+material+material_desc or \
			vals.get('name')
	return res

    def create(self, cr, uid, vals, context={}):
	if vals:
	    manufacturer = vals.get('manufacturer_id') and self.pool.get('manufacturer.master').read(cr, uid, [vals['manufacturer_id']], ['code'])[0]['code'] or False
	    vals.update({
			'am_ean13': manufacturer and manufacturer+vals['default_code'] or '',
			'state': 'sellable',
	    })
        return super(inherited_product, self).create(cr, uid, vals, context)

    _columns = {
        'description_name': fields.function(get_description_name, type='char', string='Specifications', store = True, help="Product Specifications"),
        'am_ean13': fields.char('EAN13 Barcode', size=13, help="AM Sports Number used for product identification."),
        #~ 'x_factor': fields.float('Multiplying Factor', help="Multiplying factor to calculate the sale price"),
        'x_factor': fields.function(_calculate_xfactor, type='float', string='Multiplying Factor', digits_compute=dp.get_precision('Product Price'), store = True, help="Multiplying factor to calculate the sale price"),
        #~ 'list_price': fields.function(_calculate_list_price, type='float', string='Sale Price', digits_compute=dp.get_precision('Product Price'), store = True, help="Base price to compute the customer price. Sometimes called the catalog price."),
	'list_price': fields.float('Sale Price', digits_compute=dp.get_precision('Product Price'), help="Base price to compute the customer price. Sometimes called the catalog price."),
        'am_average_cost': fields.function(_calculate_avg_cost, type='float', string='Average Inventory Val.', digits_compute=dp.get_precision('Product Price'), store = False, help="Average inventory valuation based on the standard and landed costs"),
	'am_avg_history': fields.one2many('am.average.cost', 'product_id', 'Purchase History'),
	'release': fields.many2one('release.master','Release'),
	'bottom_braket': fields.many2one('bottom.braket.master','Bottom Braket'),
	'finish': fields.many2many('finish.master','finish_product_rel','finish_id','product_id','Finish'),
	'activity_id': fields.many2many('activity.master','activity_product_rel','activity_id','product_id','Activity'),
	'gender_id': fields.many2many('gender.master','gender_product_rel','gender_id','product_id','Gender'),
    }

    _defaults = {
        'default_code': _get_default_code,
	'list_price': 1,
    }

inherited_product()
