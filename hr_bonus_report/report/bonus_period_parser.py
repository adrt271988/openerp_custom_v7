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
            'get_period': self.get_period,
            'get_now': self.get_now,
            'cr': cr,
            'uid': uid,
            'g_context': context,
        })

    def get_now(self):
        return time.strftime("%Y-%m-%d")

    def get_period(self):
        return self.localcontext['period']

    def get_rubro(self, codigo_rubro, lista_rubros):
        for rubro in lista_rubros:
            if rubro.code == codigo_rubro:
                return rubro.total
        return False

    def get_days(self, day, input_list):
        for d in input_list:
            if d.name == day:
                return d.amount
        return False

    def get_extra_hours_amount(self, key_text, input_list):
        for input_item in input_list:
            if input_item.name == key_text:
                return input_item.amount
        return 0

    def get_sum_startswith(self, start_text, category_list):
        """
        Find non predefined rules starting with a string. i.e. Advances

        :param start_text: Prefix string to search in category name
        :param category_list: Payslip's categories
        """
        amount = 0
        for cat in category_list:
            if cat.name.startswith(start_text):
                amount += cat.total
        return amount

    BENEFITS = [
        'PRESTAMO_QUIROGRAFARIO',
        'PROV FOND RESERV',
        'HORA_EXTRA_REGULAR',
        'BONO',
        'COMISION',
        'SUBT_INGRESOS',
        'SUBT_TOTINGRESOS',
        'SUBT_TOTINGRESOS',
        'PRESTAMOS_HIPOTECARIOS',
        'HORA_EXTRA_REGULAR',
        'HORA_EXTRA_EXTRAORDINARIA',
        'Otros_Ingresos',
        'IESSPERSONAL 9.45',
        'IESSPATRONAL 12.15',
        'PROV DTERCERO',
        'PROV DCUARTO',
        'SUBT_EGRESOS',
        'SUBT_NET',
        'ALIMENTACION',  # Used for *Restaurant* TODO: Check if this is correct
        'BASIC'
    ]

    # suma SUBT_INGRESOS sin beneficios
    # suma SUBT_TOTINGRESOS con beneficios

    DAYS = [u'Número de días calendario trabajados (1-30) [días]']
    OVERTIME_REGULAR = u"Numero de Horas Extras Ordinarias (150%) [horas"
    OVERTIME_IRREGULAR = u"Numero de Horas Extras Extraordinarias (200%) [horas"
    ADVANCE = u"Employee Credit"
    LOANS = u"Préstamo Empleados"

    def get_employees(self, payslips):
        employee_benefits = {}

        # Create employee dictionary.. with all zeros
        for payslip in payslips:
            if payslip.employee_id.id not in employee_benefits:
                employee_benefits[payslip.employee_id.id] = {}
                employee_benefits[payslip.employee_id.id]['name'] = payslip.employee_id.name
                employee_benefits[payslip.employee_id.id]['cedula'] = payslip.employee_id.identification_id
                employee_benefits[payslip.employee_id.id]['department'] = payslip.employee_id.department_id.name
                employee_benefits[payslip.employee_id.id]['job'] = payslip.employee_id.job_id.name
                employee_benefits[payslip.employee_id.id]['admission_date'] = payslip.employee_id.fecha_de_ingreso
                # TODO: Se ha usado el salario definido en el contrato como *Sueldo IESS* asegurarse que es correcto
                employee_benefits[payslip.employee_id.id]['iess_salary'] = payslip.contract_id.wage
                for benefit in self.BENEFITS:
                    employee_benefits[payslip.employee_id.id][benefit] = 0
                for d in self.DAYS:
                    employee_benefits[payslip.employee_id.id]['DIAS_TRABAJADOS'] = 0
                employee_benefits[payslip.employee_id.id]['DIAS_NO_TRABAJADOS'] = 0
                employee_benefits[payslip.employee_id.id]['OVERTIME_REGULAR_HOURS'] = self.get_extra_hours_amount(
                    self.OVERTIME_REGULAR, payslip.input_line_ids
                )
                employee_benefits[payslip.employee_id.id]['OVERTIME_IRREGULAR_HOURS'] = self.get_extra_hours_amount(
                    self.OVERTIME_IRREGULAR, payslip.input_line_ids
                )
                employee_benefits[payslip.employee_id.id]['total_advance'] = 0
                employee_benefits[payslip.employee_id.id]['total_loans'] = 0

        # build the sums
        for payslip in payslips:
            for benefit in self.BENEFITS:
                amount = self.get_rubro(benefit, payslip.details_by_salary_rule_category)
                if amount:
                    employee_benefits[payslip.employee_id.id][benefit] += amount

            employee_benefits[payslip.employee_id.id]['total_advance'] += self.get_sum_startswith(
                self.ADVANCE, payslip.details_by_salary_rule_category
            )
            employee_benefits[payslip.employee_id.id]['total_loans'] += self.get_sum_startswith(
                self.LOANS, payslip.details_by_salary_rule_category
            )

            for day in self.DAYS:
                amount = self.get_days(day, payslip.input_line_ids)
                if amount:
                    employee_benefits[payslip.employee_id.id]['DIAS_TRABAJADOS'] += amount

            employee_benefits[payslip.employee_id.id]['DIAS_NO_TRABAJADOS']=30-employee_benefits[payslip.employee_id.id]['DIAS_TRABAJADOS']

        employee = []
        for keys, values in employee_benefits.items():
            employee.append(values)

        employee = sorted(employee, key=itemgetter('name'))

        cont = 1
        for secuencia in range(len(employee)):
            employee[secuencia].update({'secuencia': cont})
            cont += 1
        return employee
