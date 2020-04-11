# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Item(models.Model):
    _name = 'cmdb.item'
    _description = 'Item de configuracion'

    name = fields.Char(string="Nombre", required=True, help='Nombre o clasificacion del equipo')
    
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
