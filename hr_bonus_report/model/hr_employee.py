# -*- coding: utf-8 -*-
from openerp.osv import fields, osv, orm
import datetime

class InheritHrEmployee(osv.osv):

    _inherit = 'hr.employee'

    _columns = {
        'sex_gender': fields.selection([('male', "M"),('female', "F")], string="Género"),
    }

InheritHrEmployee()
