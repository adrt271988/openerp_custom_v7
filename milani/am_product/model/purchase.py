from osv import fields, osv
from tools.translate import _

import openerp.addons.decimal_precision as dp

class am_purchase_order(osv.osv):

    _inherit = "purchase.order"

    def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
	res = super(am_purchase_order, self)._prepare_inv_line(cr, uid, account_id, order_line, context)
	res.update({'add_cost':order_line.add_cost and order_line.add_cost or 0.00})
        return res

    def action_done(self, cr, uid, ids, context=None):
	avg_obj = self.pool.get('am.average.cost')
	purchase = self.browse(cr, uid, ids[0], context)
	for line in purchase.order_line:
	    add_cost = line.add_cost and line.add_cost or 0.00
	    avg_obj.create(cr, uid, {
					'product_id': line.product_id.id,
					'standard_cost': line.price_unit,
					'landed_cost': add_cost,
					'unit_landed_cost': float(line.add_cost/line.product_qty),
					'quantity': line.product_qty,
					'amount': float((line.price_unit*line.product_qty)+add_cost),
					'date': purchase.date_order,
	    })
        self.write(cr, uid, ids, {'state':'done'}, context=context)
        return True

    _columns = {
        'order_line': fields.one2many('purchase.order.line', 'order_id', 'Order Lines', states={'done':[('readonly',True)]}),
    }
    
am_purchase_order()

class am_purchase_order_line(osv.osv):

    _inherit = "purchase.order.line"

    def _amount_line(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        for line in self.browse(cr, uid, ids, context=context):
            taxes = tax_obj.compute_all(cr, uid, line.taxes_id, line.price_unit, line.product_qty, line.product_id, line.order_id.partner_id)
            cur = line.order_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
	    res[line.id] += line.add_cost
        return res

    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, context=None):
	on_change = super(am_purchase_order_line, self).onchange_product_id(cr, uid, ids, pricelist_id, product_id, qty, uom_id,
			    partner_id, date_order, fiscal_position_id, date_planned,
			    name, price_unit, context)
	if product_id:
	    if on_change['value'].get('name'):
		on_change['value']['name'] = self.pool.get('product.product').browse(cr, uid, product_id).description_name
	return on_change

    _columns = {
        'add_cost': fields.float('Additional Costs', help="Additional Costs (Freight, duties, insurance, etc.)"),
	'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
    }
    
am_purchase_order_line()

class am_average_cost(osv.osv):
    """
    AM Sporst Average Cost
    """
    _name = "am.average.cost"
        
    _columns = {
        'product_id' : fields.many2one('product.product', 'Product', required=True ),
        'standard_cost': fields.float('Standard Cost', help="Total Purchase Cost",required=True),
        'landed_cost': fields.float('Landed Cost', help="Total Purchase Cost",required=True),
        'unit_landed_cost': fields.float('Unit Landed Cost', help="Unit Landed Cost",required=True),
        'amount': fields.float('Total Purchase Cost', help="Total Purchase Cost",required=True),
        'quantity': fields.float('Purchased Product Quantity', required=True),
        'date': fields.date('Purchase Date', required=True),
    }

am_average_cost()
