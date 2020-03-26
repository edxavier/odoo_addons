# -*- coding: utf-8 -*-
{
    'name': "Monitorizacion de equipos de red",

    'summary': """
        Seguimiento de uso de recursos de equipos en red
        """,

    'description': """
        Se registra datos de los recursos como memoria y procesador para lelvar un historial y tener informacion
        actualizada
    """,

    'author': "Eder Xavier Rojas",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Network',
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
