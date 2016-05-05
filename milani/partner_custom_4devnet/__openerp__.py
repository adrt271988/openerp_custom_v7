# -*- coding: utf-8 -*-

{
    'name' : 'Partner Custom 4devnet',
    'version' : '0.1',
    "author": "4devnet.com",
    "website": "http://www.4devnet.com",
    "category" : "Generic Modules",
    "description": """
This module add the custom fields are added on partner screen.
    """,
    'depends' : ['base','sale','purchase','crm_partner_assign'],

    "data" : [
        'wizard/send_mail_message_view.xml',
        'view/partner_custom_view.xml',
        'view/customer_data_migration_view.xml',
        'view/customer_sequence.xml',
            ],
    "css":[
        '',   
        ] ,       
    'installable': True,
    'auto_install': False,
    'application': True,
}
