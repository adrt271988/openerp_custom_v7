# -*- encoding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import decimal_precision as dp
import pooler
import time
import math

class product_attribute(osv.osv):
    '''Product Attribute Model'''
    _name = 'product.attribute'
    
    _columns = {
        'name': fields.char('Complete Name',help="Product Complete Name"),
    }

product_attribute()

class am_attribute_inherited_product(osv.osv):
        
    _inherit = 'product.product'

    def name_get(self, cr, uid, ids, context=None):
        res = super(am_attribute_inherited_product,self).name_get(cr, uid, ids, context=context)
        result = []
        for p in res:
            product = self.browse(cr, uid, p[0], context=context)
            name = '[%s] %s'%(product.default_code,product.description_name)
            mytuple = (p[0],name)
            result.append(mytuple)
        return result

    _columns = {
        'attribute_id': fields.many2one('product.attribute','Product Group'),
    }

am_attribute_inherited_product()
