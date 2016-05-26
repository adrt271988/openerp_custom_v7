# -*- coding: utf-8 -*-
from openerp.osv import fields, osv, orm
import datetime

class HrBonusReporWizard(osv.osv_memory):

    _name = 'hr.bonus.report.wizard'

    def create_report(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids)[0]
        date_from = wizard.from_period.date_start
        date_to = wizard.to_period.date_stop
        report_type = wizard.report_type
        report_name = "bonus_report"
        if report_type == 'PROV DTERCERO':
            report_name = "bonus_tercero_report"
        elif report_type == 'PROV DCUARTO':
            report_name = "bonus_cuarto_report"
        payslip_ids = []
        employee_ids = [employee.id for employee in wizard.employee_ids]
        if employee_ids:
            payslip_ids = self.pool.get('hr.payslip').search(cr, uid, [
                ('employee_id', 'in', employee_ids),
                ('state', 'not in', ['draft']),
                ('date_to', '>=', date_from),
                ('date_to', '<=', date_to),
            ], order='employee_id,period_id', context=context)
        else:
            payslip_ids = self.pool.get('hr.payslip').search(cr, uid, [
                ('state', 'not in', ['draft']),
                ('date_to', '>=', date_from),
                ('date_to', '<=', date_to),
            ], context=context)
        if not payslip_ids:
            raise orm.except_orm("Informacion", "No se encontraron nominas para los valores seleccionados")
        context = {
            'from_period': wizard.from_period.name,
            'to_period': wizard.to_period.name,
            'date_from': date_from,
            'date_to': date_to,
            'report_type': report_type,
            'payslips': payslip_ids
        }
        return {
            'type': 'ir.actions.report.xml',
            'context': context,
            'report_name': report_name,
            'datas': {
                'ids': payslip_ids
            }
        }

    _columns = {
        'period_id': fields.many2one("account.period", string="Periodo"),
        'from_period': fields.many2one("account.period", string="Periodo Inicio"),
        'to_period': fields.many2one("account.period", string="Periodo Fin"),
        'report_type': fields.selection([('PROV DTERCERO', "Tercero"),('PROV DCUARTO', "Cuarto"),('all',"Todo")], string="Tipo de Reporte", required=True),
        'employee_ids': fields.many2many('hr.employee', 'hr_bonus_report_wizard_employee_rel', 'wizard_id', 'employee_id', string="Empleados"),
        'date_from': fields.date("Desde"),
        'date_to': fields.date("Hasta"),
    }

    _defaults = {
        'report_type': 'third',
    }

HrBonusReporWizard()
