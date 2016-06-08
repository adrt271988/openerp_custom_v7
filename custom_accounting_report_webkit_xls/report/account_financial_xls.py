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

import xlwt
import time
from datetime import date
from report import report_sxw
from report_xls.report_xls import report_xls
from report_xls.utils import rowcol_to_cell
from account_financial_report_webkit.report.common_balance_reports import CommonBalanceReportHeaderWebkit
from account_financial_report_webkit.report.webkit_parser_header_fix import HeaderFooterTextWebKitParser
from tools.translate import _
import logging
_logger = logging.getLogger(__name__)

from datetime import datetime
from openerp import pooler

def sign(number):
    return cmp(number, 0)


class BalanceSheetWebkit(report_sxw.rml_parse, CommonBalanceReportHeaderWebkit):

    def __init__(self, cursor, uid, name, context):
        super(BalanceSheetWebkit, self).__init__(cursor, uid, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.cursor = self.cr
        user_brw = self.pool.get('res.users').browse(self.cr, uid, uid, context=context)
        company = user_brw.company_id
        report = self.pool.get('account.financial.report').browse(self.cr, uid, context['default_account_report_id'], context = context)
        report_name = report.name.upper()
        header_report_name = ' - '.join((report_name, company.name, company.currency_id.name))

        footer_date_time = self.formatLang(str(datetime.today()), date_time=True)

        self.localcontext.update({
            'cr': cursor,
            'uid': uid,
            'user': user_brw,
            'report_name': report_name,
            'display_account': self._get_display_account,
            'display_account_raw': self._get_display_account_raw,
            'filter_form': self._get_filter,
            'target_move': self._get_target_move,
            'display_target_move': self._get_display_target_move,
            'accounts': self._get_accounts_br,
            'additional_args': [
                ('--header-font-name', 'Helvetica'),
                ('--footer-font-name', 'Helvetica'),
                ('--header-font-size', '10'),
                ('--footer-font-size', '6'),
                ('--header-left', header_report_name),
                ('--header-spacing', '2'),
                ('--footer-left', footer_date_time),
                ('--footer-right', ' '.join((_('Page'), '[page]', _('of'), '[topage]'))),
                ('--footer-line',),
            ],
        })

    def set_context(self, objects, data, ids, report_type=None):
        """Populate a ledger_lines attribute on each browse record that will be used
        by mako template"""
        objects, new_ids, context_report_values = self.compute_balance_data(data)

        self.localcontext.update(context_report_values)

        return super(BalanceSheetWebkit, self).set_context(objects, data, new_ids,
                                                            report_type=report_type)

    

#~ HeaderFooterTextWebKitParser('report.account.account_report_trial_balance_webkit',
                             #~ 'account.account',
                             #~ )

class account_financial_xls(report_xls):
    column_sizes = [12,60,17,17,17,17,17,17]

    def generate_xls_report(self, _p, _xs, data, objects, wb):
        ws = wb.add_sheet(_p.report_name[:31])
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0 # Landscape
        ws.fit_width_to_pages = 1
        row_pos = 0

        account_obj = self.pool.get('account.account')
        currency_obj = self.pool.get('res.currency')
        ids2 = self.pool.get('account.financial.report')._get_children_by_order(self.cr, self.uid, [data['form']['account_report_id'][0]], context=data['form']['used_context'])
        lines = []
        for report in self.pool.get('account.financial.report').browse(self.cr, self.uid, ids2, context=data['form']['used_context']):
            vals = {
                'code': '',
                'name': report.name,
                'balance': report.balance * report.sign or 0.0,
                'type': 'report',
                'level': bool(report.style_overwrite) and report.style_overwrite or report.level,
                'account_type': report.type =='sum' and 'view' or False, #used to underline the financial report balances
            }
            if data['form']['debit_credit']:
                vals['debit'] = report.debit
                vals['credit'] = report.credit
            if data['form']['enable_filter']:
                vals['balance_cmp'] = self.pool.get('account.financial.report').browse(self.cr, self.uid, report.id, context=data['form']['comparison_context']).balance * report.sign or 0.0
            lines.append(vals)
            account_ids = []
            if report.display_detail == 'no_detail':
                continue
            account_ids = account_obj.search(self.cr, self.uid, [('user_type','in', [x.id for x in report.account_type_ids])])
            if account_ids:
                for account in account_obj.browse(self.cr, self.uid, account_ids, context=data['form']['used_context']):
                    if report.display_detail == 'detail_flat' and account.type == 'view':
                        continue
                    flag = False
                    vals = {
                        'name': account.name,
                        'code': account.code,
                        'account_id': account.id,
                        'balance':  account.balance != 0 and account.balance * report.sign or account.balance,
                        'type': 'account',
                        'level': report.display_detail == 'detail_with_hierarchy' and min(account.level + 1,6) or 6, #account.level + 1
                        'account_type': account.type,
                    }

                    if data['form']['debit_credit']:
                        vals['debit'] = account.debit
                        vals['credit'] = account.credit
                    if not currency_obj.is_zero(self.cr, self.uid, account.company_id.currency_id, vals['balance']):
                        flag = True
                    if data['form']['enable_filter']:
                        vals['balance_cmp'] = account_obj.browse(self.cr, self.uid, account.id, context=data['form']['comparison_context']).balance * report.sign or 0.0
                        if not currency_obj.is_zero(self.cr, self.uid, account.company_id.currency_id, vals['balance_cmp']):
                            flag = True
                    if flag:
                        lines.append(vals)
        
        # set print header/footer
        ws.header_str = self.xls_headers['standard']
        ws.footer_str = self.xls_footers['standard']

        # cf. account_report_trial_balance.mako  
        initial_balance_text = {'initial_balance': _('Computed'), 'opening_balance': _('Opening Entries'), False: _('No')}

        # Title
        cell_style = xlwt.easyxf(_xs['xls_title'])
        report_name =  ' - '.join([_p.report_name.upper(), _p.company.partner_id.name, _p.company.currency_id.name])
        c_specs = [
            ('report_name', 1, 0, 'text', report_name),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=cell_style)

        # write empty row to define column sizes
        c_sizes = self.column_sizes
        c_specs = [('empty%s'%i, 1, c_sizes[i], 'text', None) for i in range(0,len(c_sizes))]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data, set_column_size=True)

        # Header Table
        cell_format = _xs['bold'] + _xs['fill_blue'] + _xs['borders_all']
        cell_style = xlwt.easyxf(cell_format)
        cell_style_center = xlwt.easyxf(cell_format + _xs['center'])
        c_specs = [
            ('fy', 1, 0, 'text', _('Año Fiscal')),
            ('df', 1, 0, 'text', _p.filter_form(data) == 'filter_date' and _('Filtros por fecha') or _('Filtros por periodo')),
            ('tm', 2, 0, 'text',  _('Movimientos destinos'), None, cell_style_center),
            ('coa', 1, 0, 'text', _('Plan de Cuentas'), None, cell_style_center),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=cell_style)

        cell_format = _xs['borders_all'] + _xs['wrap'] + _xs['top']
        cell_style = xlwt.easyxf(cell_format)
        cell_style_center = xlwt.easyxf(cell_format + _xs['center'])
        c_specs = [
            ('fy', 1, 0, 'text', _p.fiscalyear.name if _p.fiscalyear else '-'),
        ]
        df = _('Desde') + ': '
        if _p.filter_form(data) == 'filter_date':
            df += _p.start_date if _p.start_date else u''
        else:
            df += _p.start_period.name if _p.start_period else u''
        df += ' ' + _('\nHasta') + ': '
        if _p.filter_form(data) == 'filter_date':
            df += _p.stop_date if _p.stop_date else u''
        else:
            df += _p.stop_period.name if _p.stop_period else u''
        c_specs += [
            ('df', 1, 0, 'text', df),
            ('tm', 2, 0, 'text', _p.display_target_move(data), None, cell_style_center),
            ('coa', 1, 0, 'text', _p.chart_account.name, None, cell_style_center),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=cell_style)

        # comparison header table
        if _p.comparison_mode in ('single', 'multiple'):
            row_pos += 1
            cell_format_ct = _xs['bold'] + _xs['fill_blue'] + _xs['borders_all']
            cell_style_ct = xlwt.easyxf(cell_format_ct)
            c_specs = [('ct', 8, 0, 'text', _('Comparisons'))]
            row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
            row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=cell_style_ct)
            cell_style_center = xlwt.easyxf(cell_format)
            for index, params in enumerate(_p.comp_params):
                c_specs = [('c', 3, 0, 'text', _('Comparison') + str(index + 1) + ' (C' + str(index + 1) + ')')]
                if params['comparison_filter'] == 'filter_date':
                    c_specs += [('f', 3, 0, 'text', _('Filtros por fecha') + ': ' + _p.formatLang(params['start'], date=True) + ' - ' + _p.formatLang(params['stop'], date=True))]
                elif params['comparison_filter'] == 'filter_period':
                    c_specs += [('f', 3, 0, 'text', _('Filtros por periodo') + ': ' + params['start'].name + ' - ' + params['stop'].name)]
                else:
                    c_specs += [('f', 3, 0, 'text', _('Año Fiscal') + ': ' + params['fiscalyear'].name)]
                row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
                row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=cell_style_center)

        row_pos += 1

        # Column Header Row
        cell_format = _xs['bold'] + _xs['fill_blue'] + _xs['borders_all'] + _xs['wrap'] + _xs['top']
        cell_style = xlwt.easyxf(cell_format)
        cell_style_right = xlwt.easyxf(cell_format + _xs['right'])
        cell_style_center = xlwt.easyxf(cell_format + _xs['center'])
        if len(_p.comp_params) == 2:
            account_span = 3
        else:
            account_span = _p.initial_balance_mode and 2 or 3
        c_specs = [
            ('code', 1, 0, 'text', _('Code')),
            ('account', account_span, 0, 'text', _('Cuenta')),
        ]
        if data['form']['debit_credit']:
            c_specs += [
                ('debit', 1, 0, 'text', _('Debe'), None, cell_style_right),
                ('credit', 1, 0, 'text', _('Haber'), None, cell_style_right),
            ]
        c_specs += [
            ('balance', 1, 0, 'text', _('Balance'), None, cell_style_right),
        ]
        if data['form']['enable_filter']:
            c_specs += [
                ('balance_cmp', 1, 0, 'text', data['form']['label_filter'], None, cell_style_right),
            ]
            
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=cell_style)
        ws.set_horz_split_pos(row_pos)

        last_child_consol_ids = []
        last_level = False

        # cell styles for account data
        view_cell_format = _xs['bold'] + _xs['fill'] + _xs['borders_all']
        view_cell_style = xlwt.easyxf(view_cell_format)
        view_cell_style_center = xlwt.easyxf(view_cell_format + _xs['center'])
        view_cell_style_decimal = xlwt.easyxf(view_cell_format + _xs['right'], num_format_str = report_xls.decimal_format)
        view_cell_style_pct = xlwt.easyxf(view_cell_format + _xs['center'], num_format_str = '0')
        regular_cell_format = _xs['borders_all']
        regular_cell_style = xlwt.easyxf(regular_cell_format)
        regular_cell_style_center = xlwt.easyxf(regular_cell_format + _xs['center'])
        regular_cell_style_decimal = xlwt.easyxf(regular_cell_format + _xs['right'], num_format_str = report_xls.decimal_format)
        regular_cell_style_pct = xlwt.easyxf(regular_cell_format + _xs['center'], num_format_str = '0')
        
        for line in lines:
            if line['level'] == 0:
                continue
            if line['account_type'] == 'view' or line['type'] == 'report':
                cell_style = view_cell_style
                cell_style_center = view_cell_style_center
                cell_style_decimal = view_cell_style_decimal
                cell_style_pct = view_cell_style_pct
            else:
                cell_style = regular_cell_style
                cell_style_center = regular_cell_style_center
                cell_style_decimal = regular_cell_style_decimal
                cell_style_pct = regular_cell_style_pct

            c_specs = [
                ('code', 1, 0, 'text', line['code']),
                ('account', account_span, 0, 'text', line['name']),
            ]
            if data['form']['debit_credit']: 
                c_specs += [
                    ('debit', 1, 0, 'number', line['debit'], None, cell_style_decimal),
                    ('credit', 1, 0, 'number', line['credit'], None, cell_style_decimal),
                ]
            c_specs += [('balance', 1, 0, 'number', line['balance'], None, cell_style_decimal)]
            if data['form']['enable_filter']:
                c_specs += [
                    ('balance_cmp', 1, 0, 'text', str(line['balance_cmp']), None, cell_style_decimal),
                ]

            row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
            row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=cell_style)
        
        # User and Date
        cell_style = xlwt.easyxf(_xs['bold'])
        c_specs = [
            ('blank_row', 1, 0, 'text', ''),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=cell_style)
        
        c_specs = [
            ('user', 1, 0, 'text', 'Usuario: %s'%_p.user.name),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=cell_style)
        
        c_specs = [
            ('date', 1, 0, 'text', 'Fecha: %s'%date.today().strftime('%d-%m-%Y')),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=cell_style)

        

account_financial_xls('report.account.financial.xls', 'account.account',
                             'addons/account_financial_report_webkit/report/templates/account_report_profit_loss.mako',
                             parser=BalanceSheetWebkit)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
