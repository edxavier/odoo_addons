# -*- coding: utf-8 -*-
{
    'name': "Gestion de la configuracion",

    'summary': """
        Registro de elementos de configuracion
        """,

    'description': """
        Se registra datos de los recursos como memoria y procesador para lelvar un historial y tener informacion
        actualizada
    """,

    'author': "Eder Xavier Rojas",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'ITIL',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
