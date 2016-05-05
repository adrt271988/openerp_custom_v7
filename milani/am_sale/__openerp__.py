# -*- coding: utf-8 -*-

{
    'name' : 'AM Sports Sale Module',
    'version' : '0.1',
    "author": "Alexander Rodriguez",
    "website": "",
    "category" : "Generic Modules",
    "description": """
    This module has the sale customizations for AM Sports.
    """,
    'depends' : ['base','sale','partner_custom_4devnet','am_discount'],

    "data" : [
		"view/am_sale_view.xml",
            ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
