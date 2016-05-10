# -*- coding: utf-8 -*-
import time
from report import report_sxw
import logging
from operator import itemgetter
_logger = logging.getLogger(__name__)


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_employees': self.get_employees,
            'get_period_from': self.get_period_from,
            'get_period_to': self.get_period_to,
            'get_now': self.get_now,
            'get_type': self.get_type,
            'cr': cr,
            'uid': uid,
            'g_context': context,
        })

    def get_type(self):
        report_type = self.localcontext['report_type']
        if report_type == 'PROV DTERCERO':
            return u'DÉCIMOS TERCEROS'
        elif report_type == 'PROV DCUARTO':
            return u'DÉCIMOS CUARTO'
        else:
            return u'DÉCIMOS'
        
    def get_now(self):
        return time.strftime("%Y-%m-%d")

    def get_period_from(self):
        return self.localcontext['from_period']
        
    def get_period_to(self):
        return self.localcontext['to_period']

    def get_days(self, day, input_list):
        for d in input_list:
            if d.code == day:
                return d.amount
        return False

    def get_gender(self, gender):
        if gender:
            return gender == 'male' and 'MASCULINO' or 'FEMENINO'
        return ""

    def get_sectorial_code(self, contract):
        if contract:
            if contract.codigo_sectorial:
                return contract.codigo_sectorial.codigo
        return ""

    def get_sum_startswith(self, start_text, category_list):
        amount = 0.00
        for cat in category_list:
            if cat.code == start_text:
                amount += cat.total
        return amount

    DAYS = [u'DIAS_TRABAJADOS']
    DTERCERO = u'PROV DTERCERO'
    DCUARTO = u'PROV DCUARTO'

    def get_employees(self, payslips):
        report_type = self.localcontext['report_type']
        employee_benefits = {}
        for payslip in payslips:
            if payslip.employee_id.id not in employee_benefits:
                employee_benefits[payslip.employee_id.id] = {}
                employee_benefits[payslip.employee_id.id]['name'] = payslip.employee_id.name
                employee_benefits[payslip.employee_id.id]['cedula'] = payslip.employee_id.identification_id
                employee_benefits[payslip.employee_id.id]['gender'] = self.get_gender(payslip.employee_id.gender)
                employee_benefits[payslip.employee_id.id]['job'] = payslip.employee_id.job_id and payslip.employee_id.job_id or ""
                employee_benefits[payslip.employee_id.id]['sectorial_code'] = self.get_sectorial_code(payslip.employee_id.contract_id)
                
                for d in self.DAYS:
                    employee_benefits[payslip.employee_id.id]['DIAS_TRABAJADOS'] = 0.00
                employee_benefits[payslip.employee_id.id]['decimo_tercero'] = 0.00
                employee_benefits[payslip.employee_id.id]['decimo_cuarto'] = 0.00

        # build the sums
        for payslip in payslips:
            if report_type in ['all','PROV DCUARTO']:
                employee_benefits[payslip.employee_id.id]['decimo_cuarto'] += self.get_sum_startswith(
                    self.DTERCERO, payslip.details_by_salary_rule_category
                )
            if report_type in ['all','PROV DTERCERO']:
                employee_benefits[payslip.employee_id.id]['decimo_tercero'] += self.get_sum_startswith(
                    self.DCUARTO, payslip.details_by_salary_rule_category
                )

            for day in self.DAYS:
                amount = self.get_days(day, payslip.input_line_ids)
                if amount:
                    employee_benefits[payslip.employee_id.id]['DIAS_TRABAJADOS'] += amount

        employee = []
        for keys, values in employee_benefits.items():
            employee.append(values)

        employee = sorted(employee, key=itemgetter('name'))

        cont = 1
        for secuencia in range(len(employee)):
            employee[secuencia].update({'secuencia': cont})
            cont += 1
        return employee
