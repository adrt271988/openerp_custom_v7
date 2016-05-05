# -*- coding: utf-8 -*-
from openerp.osv import fields, osv, orm
import datetime
import xlwt
from xlsxwriter.workbook import Workbook
import base64

class HrBonusReporWizard(osv.osv_memory):

    _name = 'hr.bonus.report.wizard'

    def create_report(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids)[0]
        date_from = wizard.from_period.date_start
        date_to = wizard.to_period.date_stop
        employee_ids = [employee.id for employee in wizard.employee_ids]
        string = employee_ids and "employee_id in %s AND"%tuple(employee_ids) or ""
        cr.execute(""" SELECT pay.period_id,pay.employee_id,em.name_related FROM hr_payslip AS pay
                        LEFT JOIN hr_employee AS em ON em.id = pay.employee_id
                        WHERE pay.employee_id in (921,794) AND pay.date_to BETWEEN '2016-01-01' AND '2016-02-29'
                        GROUP BY pay.employee_id,em.name_related,pay.period_id
                        ORDER BY em.name_related"""%(string,date_from,date_to))
        res = cr.dictfetchall()
        print '******',res
        if employee_ids:
            paysplip_ids = self.pool.get('hr.payslip').search(cr, uid, [
                ('employee_id', 'in', employee_ids),
                ('state', 'not in', ['draft']),
                ('date_to', '>=', date_from),
                ('date_to', '<=', date_to),
            ], order='employee_id,period_id', context=context)
        else:
            paysplip_ids = self.pool.get('hr.payslip').search(cr, uid, [
                ('state', 'not in', ['draft']),
                ('date_to', '>=', date_from),
                ('date_to', '<=', date_to),
            ], order='period_id', context=context)
        if not paysplip_ids:
            raise orm.except_orm("Informacion", "No se encontraron nominas para los valores seleccionados")
        context = {
            'from_period': wizard.from_period.id,
            'to_period': wizard.to_period.id,
            'date_from': date_from,
            'date_to': date_to,
            'report_type': wizard.report_type,
        }
        print paysplip_ids
        return True
        #~ return {
            #~ 'type': 'ir.actions.report.xml',
            #~ 'context': context,
            #~ 'report_name': 'bonus_period_report',
            #~ 'datas': {
                #~ 'ids': paysplip_ids
            #~ }
        #~ }

    _columns = {
        'period_id': fields.many2one("account.period", string="Periodo"),
        'from_period': fields.many2one("account.period", string="Periodo Inicio"),
        'to_period': fields.many2one("account.period", string="Periodo Fin"),
        'report_type': fields.selection([('third', "Tercero"),('fourth', "Cuarto"),('all',"Todo")], string="Tipo de Reporte", required=True),
        'employee_ids': fields.many2many('hr.employee', 'hr_bonus_report_wizard_employee_rel', 'wizard_id', 'employee_id', string="Empleados"),
        'date_from': fields.date("Desde"),
        'date_to': fields.date("Hasta"),
    }

    _defaults = {
        'report_type': 'third',
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

    #~ _constraints = [
        #~ (_check_date, "La fecha de inicio debe ser mayor que la fecha fin", ['date_from','date_to']),
    #~ ]

HrBonusReporWizard()
