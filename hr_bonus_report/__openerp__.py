# -*- coding: utf-8 -*-
{
    'name': "Reporte de Décimos",
    'summary': "Reporte de Décimos Terceros y Cuartos",
    'version': '0.1',
    'description': """
Reporte de Decimos.
===================

Caracteríscas Principales:
--------------------------
    * Reporte de Décimos Terceros y Cuartos de los empleados
    * Filtros por periodo
    * Formato de Reporte: Excel (.xls)
    """,
    'author': 'Alexander Rodriguez <adrt271988@gmail.com>',
    "depends": ['ecua_hr'],
    #~ "data": [
        #~ 'wizard/hr_bonus_report_wizard.xml',
    #~ ],
    "update_xml": [
        'wizard/hr_bonus_report_wizard.xml',
    ],
    'installable': True,
    "active": False,
}
