# -*- coding: utf-8 -*-
# from odoo import http


# class C:\odooAddons\websiteMisc(http.Controller):
#     @http.route('/c:\odoo_addons\website_misc/c:\odoo_addons\website_misc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/c:\odoo_addons\website_misc/c:\odoo_addons\website_misc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('c:\odoo_addons\website_misc.listing', {
#             'root': '/c:\odoo_addons\website_misc/c:\odoo_addons\website_misc',
#             'objects': http.request.env['c:\odoo_addons\website_misc.c:\odoo_addons\website_misc'].search([]),
#         })

#     @http.route('/c:\odoo_addons\website_misc/c:\odoo_addons\website_misc/objects/<model("c:\odoo_addons\website_misc.c:\odoo_addons\website_misc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('c:\odoo_addons\website_misc.object', {
#             'object': obj
#         })
