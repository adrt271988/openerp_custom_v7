from osv import fields, osv
from tools.translate import _

import openerp.addons.decimal_precision as dp

class am_discount(osv.osv):

    _name = "am.discount"
    _order = "value asc"
    _description = "Discounts for sale/purchase orders"
    
    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        res = super(am_discount,self).default_get(cr, uid, fields, context=context) 
        if 'order_type' in context:
            res.update({'order_type': context['order_type']})
        return res
        
    _columns = {
        'name': fields.char('Name', size=100, required=True, select=True),
        'order_type': fields.selection([
            ('sale', 'Sale Order'),
            ('purchase', 'Purchase Order'),
            ], 'Document', required=True, help="The document where the discount wil be apply"),
        'value': fields.float('Discount (%)', digits_compute=dp.get_precision('Discount'),help="Percent value"),
        'note': fields.text('Description', help="Discount description (how, when, special conditions, etc.)"),
        'active': fields.boolean('Active', help="If the active field is set to False, it will allow you to hide the discount without removing it."),
        'sale_line': fields.many2one('sale.order.line', 'Sale Order Line'),
        'invoice_line': fields.many2one('account.invoice.line', 'Invoice Line'),
        }
        
    _defaults = {
        'active' : True,
    }

am_discount()
