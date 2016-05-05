# -*- coding: utf-8 -*-

{
    'name' : 'AM Sports Product Grouping Module',
    'version' : '0.1',
    "author": "Alexander Rodriguez",
    "website": "",
    "category" : "Generic Modules",
    "description": """
This module helps to find products by name in POs, SOs and Invoices
    """,
    'depends' : ['am_product'],

    "data" : [
        "view/product_attribute_view.xml",
        "view/product_view.xml",
        "view/purchase_view.xml",
        "view/sale_view.xml",
            ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
