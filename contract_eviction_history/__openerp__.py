# -*- coding: utf-8 -*-
{
    'name': "Historial de Contrato por Desahucio",
    'summary': "Historial de Contrato por Desahucio",
    'version': '0.1',
    'description': """
Historial de Contrato por Desahucio
===================================

Caracteríscas Principales:
--------------------------
    * En las reglas salariales de: “Fondos de Reserva Pagados”, “Fondos de Reserva Retenidos” y “Gerente - Fondos de Reserva Retenidos” se modifican para validar si el empleado tiene historial de Contrato.
    * Se agrega campo 'Tiene historial de contrato' en la ficha de Contrato de Empleado.
    """,
    'author': 'Alexander Rodriguez <adrt271988@gmail.com>',
    "depends": ['ecua_hr','ecua_hr_data'],
    "update_xml": [
        'view/hr_contract_view.xml',
    ],
    'installable': True,
    "active": False,
}
