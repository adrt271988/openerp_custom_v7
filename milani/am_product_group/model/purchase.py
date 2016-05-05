from osv import fields, osv
from tools.translate import _

import openerp.addons.decimal_precision as dp

class am_attribute_purchase_order_line(osv.osv):

    _inherit = "purchase.order.line"

    def onchange_attribute_id(self, cr, uid, ids, attribute_id, context = None):
	res = {}
	if attribute_id:
	    res = {'domain': {'product_id': [('attribute_id','=',attribute_id)]}}
	return res

    _columns = {
        'attribute_id': fields.many2one('product.attribute','Product Group'),
    }
    
am_attribute_purchase_order_line()
