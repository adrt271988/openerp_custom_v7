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

from osv import fields, osv
#import logging
#_logger = logging.getLogger(__name__)

class account_financial_report(osv.osv_memory):
    _inherit = 'accounting.report'
       
    def xls_export(self, cr, uid, ids, context=None):
        res= self.check_report(cr, uid, ids, context=context)
        return res

    def _print_report(self, cr, uid, ids, data, context=None):
        context = context or {}
        if context.get('xls_export'):
            # we update form with display account value
            data = self.pre_print_report(cr, uid, ids, data, context=context)
            cuenta=self.browse(cr, uid,ids, context=None)
            data['form']['type'] = cuenta[0].type
            data['form']['niveles']=cuenta[0].niveles


            return {'type': 'ir.actions.report.xml',
                    'report_name': 'account.account_report_financial_xls',
                    'datas': data}
        else:
            return super(account_financial_report, self)._print_report(cr, uid, ids, data, context=context)

    # def check_report(self, cr, uid, ids, context=None):
    #     res = {}
    #     # super('accounting.report', self).check_report(cr, uid, ids, context)
    #     # nueva_var=res['datas']['form']['comparison_context']
    #     return super('accounting.report', self).check_report(cr, uid, ids, context)
    
account_financial_report()
