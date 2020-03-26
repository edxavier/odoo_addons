# -*- coding: utf-8 -*-
# from odoo import http


# class Net(http.Controller):
#     @http.route('/net/net/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/net/net/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('net.listing', {
#             'root': '/net/net',
#             'objects': http.request.env['net.net'].search([]),
#         })

#     @http.route('/net/net/objects/<model("net.net"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('net.object', {
#             'object': obj
#         })
