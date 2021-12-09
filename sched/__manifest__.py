# -*- coding: utf-8 -*-
{
    'name': "Gestion de horario laboral",

    'summary': """
        Gestion de matris de horario y rotacion del mismo""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Eder Rojas",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Horario',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts', 'cmdb'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'reports/sched.xml',
        'reports/formats.xml',
        'data/sequences.xml',
        'data/defaults.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
