# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Customer(models.Model):
    _name = 'cmdb.customer'
    _description = 'Posicion de usuario'

    name = fields.Char(string="Nombre", help='Nombre', required=True)
    building = fields.Many2one('cmdb.building', ondelete="cascade", string='Edificio', domain=[('active', '=', True)])
    office = fields.Many2one('cmdb.office', ondelete="cascade", string='Oficina', domain=[('active', '=', True)])
    active = fields.Boolean(default=True)
