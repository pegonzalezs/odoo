# -*- coding: utf-8 -*-
from odoo import http

# class Coop(http.Controller):
#     @http.route('/coop/coop/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/coop/coop/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('coop.listing', {
#             'root': '/coop/coop',
#             'objects': http.request.env['coop.coop'].search([]),
#         })

#     @http.route('/coop/coop/objects/<model("coop.coop"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('coop.object', {
#             'object': obj
#         })