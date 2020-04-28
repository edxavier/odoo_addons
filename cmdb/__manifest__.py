# -*- coding: utf-8 -*-
{
    'name': "Gestion de la configuracion",

    'summary': """
        Registro de elementos de configuracion
        """,

    'description': """
        Base de datos de todos los elementos de configuracion, servicios, componentes y todo lo relacionado en el funcionamiento del negocio
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
        'views/lists.xml',
        'views/forms.xml',
        'data/secuences.xml',
        'data/defaults.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
