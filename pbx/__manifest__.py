# -*- coding: utf-8 -*-
{
    'name': "Gestion PBX",

    'summary': """
        Gestion de extensiones telefonicas y cableado""",

    'description': """
        Gestion de extensiones y puntos de cableado estructurado de telefonia
    """,

    'author': "Xavier Rojas",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Telefonia',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',  'mail'],

    # always loaded
    'data': [
        'data/locations.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/filters.xml',
        'views/form.xml',
        'views/list.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
