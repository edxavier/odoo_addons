# -*- coding: utf-8 -*-
{
    'name': "Gestion Operacional",

    'summary': """
        Registro de Incidentes, cambios e interrupciones de equipos y servicios
        """,

    'description': """
        Base de datos de todos los elementos de Registro de Incidentes, cambios e interrupciones de equipos y servicios
    """,

    'author': "Eder Xavier Rojas",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'ITIL',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'cmdb', 'mail'],

    # always loaded
    'data': [
        #'security/security.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
        #'views/templates.xml',
        'views/lists.xml',
        'views/wizards.xml',
        'views/actions.xml',
        'views/forms.xml',
        'data/secuences.xml',

        #'data/defaults.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
