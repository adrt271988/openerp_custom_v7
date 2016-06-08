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
{
    'name': 'Categorización de Pagos',
    'version': '0.1',
    'author': 'Alexander Rodriguez <adrt271988@gmail.com>',
    'category': 'Accounting',
    'description': """ 
    Categorización de Pagos:
        - Este módulo se encarga de agregar categorías a los pagos de clientes/proveedores
    """,
    'depends': ['account_voucher'],
    'demo_xml': [],
    'init_xml': [],
    'update_xml' : [
        'view/account_voucher_category_view.xml',
    ],
    'active': False,
    'installable': True,
}
