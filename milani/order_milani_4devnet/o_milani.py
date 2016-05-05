# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

from openerp.osv import fields, osv


class purchase_order_line(osv.osv):
    _inherit = 'purchase.order.line'
    _columns = {
                'category_id':fields.many2one('product.category','Category'),
                'brand_id':fields.many2one('partner.brand','Brand'),
                'series':fields.char('Series'), 
                'model':fields.char('Model'),
                'activity_id' : fields.many2one('activity.master','Activity'),                   
                'type_id' :fields.many2one('type.master','Type'),   
                'specialty_id':fields.many2one('specialty.master','Specialty'),
                'wheel_size_id':fields.many2one('wheel.size.master','Wheel-size'),
                'size_id':fields.many2one('size.master','Size'),
                'discipline_id' :fields.many2one('discipline.master','Discipline'),
                'sport':fields.char('Sport'),
                'spcl_tech':fields.char('Special Technology'),
                'material_desc':fields.char('Material Desc.'),
                'material':fields.char('Material'), 
                'color_id':fields.many2one('color.master','Color'),                 
                'design_id':fields.many2one('design.master','Design'),
                'seat_id':fields.many2one('seat.post.diameter.master','Seat-Post-Diameter'),
                'bar_id':fields.many2one('bar.bore.diameter.master','Bar-Bore-Diameter'),
                'rake_id':fields.many2one('rake.master','Rake'),
                'width_oo_id':fields.many2one('width.oo.master','Width OO'),
                'taxle_id':fields.many2one('taxle.master','T-axle'),
                'brakes_id':fields.many2one('brakes.master','Brakes'),
                'head_tube_id':fields.many2one('head.tube.master','Head-Tube'),
                'width_id':fields.many2one('width.master','Width'),
                'ussize_id':fields.many2one('ussize.master','US-size'),
                'manufacturer_id':fields.many2one('manufacturer.master','Manufacturer'),
                    
                }

purchase_order_line()
class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    _columns = {
                'category_id':fields.many2one('product.category','Category'),
                'brand_id':fields.many2one('partner.brand','Brand'),
                'series':fields.char('Series'), 
                'model':fields.char('Model'),
                'activity_id' : fields.many2one('activity.master','Activity'),                   
                'type_id' :fields.many2one('type.master','Type'),   
                'specialty_id':fields.many2one('specialty.master','Specialty'),
                'wheel_size_id':fields.many2one('wheel.size.master','Wheel-size'),
                'size_id':fields.many2one('size.master','Size'),
                'discipline_id' :fields.many2one('discipline.master','Discipline'),
                'sport':fields.char('Sport'),
                'spcl_tech':fields.char('Special Technology'),
                'material_desc':fields.char('Material Desc.'),
                'material':fields.char('Material'), 
                'color_id':fields.many2one('color.master','Color'),                 
                'design_id':fields.many2one('design.master','Design'),
                'seat_id':fields.many2one('seat.post.diameter.master','Seat-Post-Diameter'),
                'bar_id':fields.many2one('bar.bore.diameter.master','Bar-Bore-Diameter'),
                'rake_id':fields.many2one('rake.master','Rake'),
                'width_oo_id':fields.many2one('width.oo.master','Width OO'),
                'taxle_id':fields.many2one('taxle.master','T-axle'),
                'brakes_id':fields.many2one('brakes.master','Brakes'),
                'head_tube_id':fields.many2one('head.tube.master','Head-Tube'),
                'width_id':fields.many2one('width.master','Width'),
                'ussize_id':fields.many2one('ussize.master','US-size'),
                'manufacturer_id':fields.many2one('manufacturer.master','Manufacturer'),
                    
                }

sale_order_line()
#domain="[('categ_id','=',category_id)]
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

