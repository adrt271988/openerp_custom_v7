# -*- coding: utf-8 -*-

{
    'name' : 'AM Sports Product Module',
    'version' : '0.1',
    "author": "Alexander Rodriguez",
    "website": "",
    "category" : "Generic Modules",
    "description": """
This module has the customizations for AM Sports.
    """,
    'depends' : ['base','product','product_mil_4devnet'],

    "data" : [
		"purchase_workflow.xml",
		"view/product_view.xml",
		"view/purchase_view.xml",
            ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
