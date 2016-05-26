from osv import fields, osv
from tools.translate import _

import openerp.addons.decimal_precision as dp

class am_account_invoice(osv.osv):

    _inherit = "account.invoice"
    
    #~ _columns = {
	#~ 'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
	#~ 'discount_ids': fields.many2many('am.discount', 'sale_line', 'order_line_id', 'discount_id', 'Discounts', readonly=True, states={'draft': [('readonly', False)]}),
	#~ 'discounted_unit_price': fields.function(_discount_unit_price, string='Disc. Unit Price', digits_compute= dp.get_precision('Account')),
        #~ }
	
am_account_invoice()

class am_account_invoice_line(osv.osv):

    _inherit = "account.invoice.line"
    
    def product_id_change(self, cr, uid, ids, product, uom_id, qty=0, name='', type='out_invoice',
				partner_id=False, fposition_id=False, price_unit=False,
				currency_id=False, context=None, company_id=None):
	on_change = super(am_account_invoice_line, self).product_id_change(cr, uid, ids, product, uom_id, qty, name, type, partner_id,
                            fposition_id, price_unit, currency_id, context, company_id)
	if product:
	    if on_change['value'].get('name'):
		on_change['value']['name'] = self.pool.get('product.product').browse(cr, uid, product).description_name
	return on_change

    def _discount_unit_price(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
	    result = line.price_unit
	    for discount in line.discount_ids:
		result -= result*(discount.value/100)
            res[line.id] = result
        return res

    def _amount_line(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        res = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        for line in self.browse(cr, uid, ids):
            #~ price = line.price_unit * (1-(line.discount or 0.0)/100.0)
	    result = line.price_unit
	    if line.discount_ids:
		for discount in line.discount_ids:
		    result -= result*(discount.value/100)
	    price = result
            taxes = tax_obj.compute_all(cr, uid, line.invoice_line_tax_id, price, line.quantity, product=line.product_id, partner=line.invoice_id.partner_id)
            res[line.id] = taxes['total']
            if line.invoice_id:
                cur = line.invoice_id.currency_id
                res[line.id] = cur_obj.round(cr, uid, cur, res[line.id])
		res[line.id] += line.add_cost or 0.00
        return res

    _columns = {
	'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
	'discount_ids': fields.many2many('am.discount', 'invoice_line', 'order_line_id', 'discount_id', 'Discounts'),
	'discounted_unit_price': fields.function(_discount_unit_price, string='Disc. Unit Price', digits_compute= dp.get_precision('Account')),
	'add_cost': fields.float('Additional Costs', help="Additional Costs (Freight, duties, insurance, etc.)"),
        }
	
am_account_invoice_line()


