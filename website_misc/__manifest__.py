# -*- coding: utf-8 -*-
{
    'name': "Utilidades para website",

    'summary': """
        Utilidades para sitio web""",

    'description': """
        Oculta el footer de promocion de la marca odoo.
    """,

    'author': "Eder Xavier Rojas",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.1',
    "application": False,
    "installable": True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/footer.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
