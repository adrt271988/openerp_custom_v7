# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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

import time
from lxml import etree
from openerp import netsvc
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp.tools import float_compare

class account_voucher_category(osv.osv):
    _name = 'account.voucher.category'

    _description = 'Accounting Voucher Categories'

    _columns = {
        'name': fields.char('Nombre', help="Nombre de la categoría", required=True),
        'type':fields.selection([
                ('customer','Clientes'),
                ('supplier','Proveedores'),
                ('both','Ambos'),
            ],'Tipo de Categoría', required=True,
            help="Tipo de categoría asociado al tipo de pago (Clientes, Proveedores o Ambos)"),
        'parent_id': fields.many2one('account.voucher.category','Categoría Padre', ondelete='cascade', help="Categoría Padre")
    }

account_voucher_category()
