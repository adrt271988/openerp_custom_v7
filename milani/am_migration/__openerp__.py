# -*- coding: utf-8 -*-

{
    'name' : 'AM Sports Migration',
    'version' : '0.1',
    "author": "Alexander Rodriguez",
    "website": "",
    "category" : "Generic Modules",
    "description": """
This module migrates the data in csv to openerp data.
    """,
    'depends' : ['base','product','am_product'],

    "data" : [
		"view/migration_view.xml",
		"wizard/product_load_category_wizard_view.xml",
		"wizard/product_load_masters_wizard_view.xml",
                "wizard/product_migration_wizard_view.xml",
            ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
