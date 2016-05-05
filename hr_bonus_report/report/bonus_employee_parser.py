# -*- coding: utf-8 -*-
import time
from report import report_sxw
import logging

_logger = logging.getLogger(__name__)


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'tmp_set': self.tmp_set,
            'tmp_get': self.tmp_get,
            'get_date_from': self.get_date_from,
            'get_date_to': self.get_date_to,
            'get_now': self.get_now,
            'get_category_amount': self.get_category_amount,
            'cr': cr,
            'uid': uid,
            'g_context': context,
            'storage': {},
        })

    def get_now(self):
        return time.strftime("%Y-%m-%d")

    def get_date_from(self):
        return self.localcontext['date_from']

    def get_date_to(self):
        return self.localcontext['date_to']

    def tmp_set(self, pair):
        if isinstance(pair, dict):
            self.localcontext['storage'].update(pair)
        return False

    def get_category_amount(self, category_code, categories):
        """Get total amount in a specified category by code from list of payroll rule. i.e. ``SUBT_TOTINGRESOS``"""
        for category in categories:
            if category.code == category_code:
                return category.total
        return 0

    def tmp_get(self, key):
        if key in self.localcontext['storage'] and self.localcontext['storage'][key]:
            return self.localcontext['storage'][key]
        return False
