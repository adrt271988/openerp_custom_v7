# -*- coding: utf-8 -*-

{
    'name' : 'AM Sports Discount Module',
    'version' : '0.1',
    "author": "Alexander Rodriguez",
    "website": "",
    "category" : "Generic Modules",
    "description": """
    This module has the discount customizations for AM Sports.
    """,
    'depends' : ['base','sale'],

    "data" : [
		"view/am_discount_view.xml",
            ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
