# -*- coding: utf-8 -*-
{
    'name': "Library Management",

    'summary': "Manage a library",

    'description': """
        Manage a library:
        * Books
        * Contacts
        * Rentals
    """,

    'author': "Antoine Guenet",
    'website': "http://www.antoineguenet.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    'application': True,

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}