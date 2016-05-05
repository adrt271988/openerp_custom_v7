# coding=utf-8
from openerp.osv import fields, osv, orm
import datetime
import xlwt
from xlsxwriter.workbook import Workbook
import base64

class HrBonusReporWizard(osv.osv_memory):

    _name = 'hr.bonus.report.wizard'

    def create_report(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids)[0]
        if wizard.report_type == 'period':
            return self.bonus_period_report(cr, uid, wizard, context)
        else:
            return self.bonus_employee_report(cr, uid, wizard, context)
        return True

    def bonus_period_report(self, cr, uid, wizard, context=None):
        if not wizard.period_id:
            raise orm.except_orm("Error", "Debe elegir un periodo")

        paysplip_ids = self.pool.get('hr.payslip').search(cr, uid, [
            ('period_id', '=', wizard.period_id.id), ('state', 'not in', ['draft'])
        ], context=context)

        if not paysplip_ids:
            raise orm.except_orm("Informacion", "No se encontraron nóminas en el periodo seleccionado")

        context = {'period': wizard.period_id.name, 'bonus_type': wizard.bonus_type}

        return {
            'type': 'ir.actions.report.xml',
            'context': context,
            'report_name': 'bonus_period_report',
            'datas': {
                'ids': paysplip_ids
            }
        }

    def employee_payslip_report(self, cr, uid, wizard, context=None):
        employee_ids = [employee.id for employee in wizard.employee_ids]
        paysplip_ids = self.pool.get('hr.payslip').search(cr, uid, [
            ('employee_id', 'in', employee_ids),
            ('state', 'not in', ['draft']),
            ('date_to', '>=', wizard.date_from),
            ('date_to', '<=', wizard.date_to),
        ], order='employee_id,period_id', context=context)
        if not paysplip_ids:
            raise orm.except_orm("Informacion", "No se encontraron nóminas para los valores seleccionados")
        context = {
            'date_from': wizard.date_from,
            'date_to': wizard.date_to,
            'bonus_type': wizard.bonus_type,
        }
        return {
            'type': 'ir.actions.report.xml',
            'context': context,
            'report_name': 'bonus_employee_report',
            'datas': {
                'ids': paysplip_ids
            }
        }

    _columns = {
        'period_id': fields.many2one("account.period", string="Periodo"),
        'bonus_type': fields.selection([('third', "Tercero"),('fourth', "Cuarto"),('all',"Todo")], string="Décimo", required=True),
        'report_type': fields.selection([('period', "Por Período"), ('employee', "Por Empleado")],string="Tipo de reporte", required=True),
        'employee_ids': fields.many2many('hr.employee', 'hr_bonus_report_wizard_employee_rel', 'wizard_id', 'employee_id', string="Empleados"),
        'date_from': fields.date("Desde"),
        'date_to': fields.date("Hasta"),
    }

    _defaults = {
        'bonus_type': 'third',
        'report_type': 'employee'
    }

    def _check_date(self, cr, uid, ids):
        for payroll_employee in self.browse(cr, uid, ids):
            date_from = payroll_employee.date_from
            date_to = payroll_employee.date_to
            if date_from and date_to:
                DATETIME_FORMAT = "%Y-%m-%d"
                dt_from = datetime.datetime.strptime(date_from, DATETIME_FORMAT)
                dt_to = datetime.datetime.strptime(date_to, DATETIME_FORMAT)
                if dt_to < dt_from:
                    return False
        return True

    _constraints = [
        (_check_date, "La fecha de inicio debe ser mayor que la fecha fin", ['date_from','date_to']),
    ]

HrBonusReporWizard()
