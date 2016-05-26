from osv import fields, osv
from tools.translate import _

import openerp.addons.decimal_precision as dp

class am_sale_order(osv.osv):

    _inherit = "sale.order"

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
	for inv_line in self.pool.get('account.invoice.line').browse(cr, uid, lines, context):
	    for line in order.order_line:
		if line.discount_ids:
		    self.pool.get('account.invoice.line').write(cr, uid, [inv_line.id], {'discount_ids':[(6,0,[x.id for x in line.discount_ids])]})
        return super(am_sale_order, self)._prepare_invoice(cr, uid, order, lines, context)
	
am_sale_order()

class am_sale_order_line(osv.osv):

    _inherit = "sale.order.line"

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
	on_change = super(am_sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty,
			    uom, qty_uos, uos, name, partner_id,
			    lang, update_tax, date_order, packaging, fiscal_position, flag, context)
	if product:
	    if on_change['value'].get('name'):
		on_change['value']['name'] = self.pool.get('product.product').browse(cr, uid, product).description_name
	return on_change

    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            #~ price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
	    result = line.price_unit
	    if line.discount_ids:
		for discount in line.discount_ids:
		    result -= result*(discount.value/100)
	    price = result
            taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, line.product_uom_qty, line.product_id, line.order_id.partner_id)
            cur = line.order_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
        return res
	
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
            
    _columns = {
	'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
	'discount_ids': fields.many2many('am.discount', 'sale_line', 'order_line_id', 'discount_id', 'Discounts', readonly=True, states={'draft': [('readonly', False)]}),
	'discounted_unit_price': fields.function(_discount_unit_price, string='Disc. Unit Price', digits_compute= dp.get_precision('Account')),
        }
	
am_sale_order_line()
