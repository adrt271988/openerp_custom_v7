# -*- coding: utf-8 -*-
{
    'name' : 'AM Sports Account Module',
    'version' : '0.1',
    "author": "Alexander Rodriguez",
    "website": "",
    "category" : "Generic Modules",
    "description": """
    This module has the account customizations for AM Sports.
    """,
    'depends' : ['base','account','am_discount','am_sale','am_product'],

    "data" : [
		"view/account_invoice_view.xml",
            ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
