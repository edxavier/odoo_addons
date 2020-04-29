# -*- coding: utf-8 -*-
# from odoo import http


# class Schd(http.Controller):
#     @http.route('/schd/schd/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/schd/schd/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('schd.listing', {
#             'root': '/schd/schd',
#             'objects': http.request.env['schd.schd'].search([]),
#         })

#     @http.route('/schd/schd/objects/<model("schd.schd"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('schd.object', {
#             'object': obj
#         })
