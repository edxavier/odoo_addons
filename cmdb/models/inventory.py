# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Asset(models.Model):
    _name = 'cmdb.asset'
    _description = 'Activo'


    @api.onchange('manufacturer')
    def manufacturerOnchange(self):
        for rec in self:
            rec.model = None
            return {'domain': {'model': [('manufacturer', '=', rec.manufacturer.id)]}}

    name = fields.Char(string="Nombre", help='Nombre o clasificacion del equipo', required=True,)
    asset_type = fields.Many2one('cmdb.asset.type', ondelete="cascade", string='Tipo', required=True, domain=[('active', '=', True)])
    location = fields.Char(string="Nombre", help='Nombre o clasificacion del equipo', required=True,)
    note = fields.Text(string="Nota", help='Descripcion')
    
    manufacturer = fields.Many2one('cmdb.manufacturer', ondelete="cascade", string='Marca', domain=[('active', '=', True)])
    model = fields.Many2one('cmdb.model', ondelete="cascade", string='Modelo')
    serie = fields.Char(string="Serie", help='Serie del Item', default="---")
    inventory = fields.Char(string="Inventario", default="---")

    owner = fields.Many2one('res.partner', ondelete="cascade", string='Propietario')
    assigned = fields.Many2one('res.partner', ondelete="cascade", string='Asignado')

    status = fields.Many2one('cmdb.asset.status', ondelete="cascade", string='Estado', required=True, domain=[('active', '=', True)])
    installed = fields.Date("Fecha de instalacion o adquisicion", )
    active = fields.Boolean(default=True, string='Activo')


