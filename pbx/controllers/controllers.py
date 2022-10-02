# -*- coding: utf-8 -*-
# from odoo import http


# class C:\odooAddons\pbx(http.Controller):
#     @http.route('/c:\odoo_addons\pbx/c:\odoo_addons\pbx/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/c:\odoo_addons\pbx/c:\odoo_addons\pbx/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('c:\odoo_addons\pbx.listing', {
#             'root': '/c:\odoo_addons\pbx/c:\odoo_addons\pbx',
#             'objects': http.request.env['c:\odoo_addons\pbx.c:\odoo_addons\pbx'].search([]),
#         })

#     @http.route('/c:\odoo_addons\pbx/c:\odoo_addons\pbx/objects/<model("c:\odoo_addons\pbx.c:\odoo_addons\pbx"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('c:\odoo_addons\pbx.object', {
#             'object': obj
#         })
