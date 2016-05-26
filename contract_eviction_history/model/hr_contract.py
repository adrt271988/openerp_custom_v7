# -*- coding: utf-8 -*-
from openerp.osv import fields, osv, orm
import datetime

class EvictionInheritHrContract(osv.osv):

    _inherit = 'hr.contract'

    _columns = {
        'contract_history': fields.boolean(string="Tiene Historial de Contrato?",help="Indique si este empleado posee historial de contrataciones"),
    }

EvictionInheritHrContract()
