# -*- coding: utf-8 -*-
{
    'name': "Modulo de mantenimiento",

    'summary': """
        Registro de las tareas de mantenimiento""",

    'description': """
        Regsitro y seguimiento a tareas de mantenimiento para los equipos
    """,

    'author': "Eder Rojas",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Mantenimiento',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','cmdb'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'security/ir.model.access.csv',
        'data/defaults.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
