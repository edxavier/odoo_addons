# -*- coding: utf-8 -*-
# from odoo import http


# class Maint(http.Controller):
#     @http.route('/maint/maint/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/maint/maint/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('maint.listing', {
#             'root': '/maint/maint',
#             'objects': http.request.env['maint.maint'].search([]),
#         })

#     @http.route('/maint/maint/objects/<model("maint.maint"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('maint.object', {
#             'object': obj
#         })
