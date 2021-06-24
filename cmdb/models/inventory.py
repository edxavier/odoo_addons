# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Asset(models.Model):
    _name = 'cmdb.asset'
    _description = 'Activo'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    @api.onchange('manufacturer')
    def manufacturerOnchange(self):
        for rec in self:
            rec.model = None
            return {'domain': {'model': [('manufacturer', '=', rec.manufacturer.id)]}}

    name = fields.Char(string="Nombre", help='Nombre o clasificacion del equipo', required=True, tracking=True)
    asset_type = fields.Many2one('cmdb.asset.type', ondelete="cascade", string='Tipo', required=True, domain=[('active', '=', True)], tracking=True)
    location = fields.Char(string="Ubicacion", required=True, tracking=True)
    note = fields.Text(string="Nota", help='Nota')
    
    manufacturer = fields.Many2one('cmdb.manufacturer', ondelete="cascade", string='Marca', domain=[('active', '=', True)], tracking=True)
    model = fields.Many2one('cmdb.model', ondelete="cascade", string='Modelo', tracking=True)
    serie = fields.Char(string="Serie", help='Serie del Item', default="---", tracking=True)
    inventory = fields.Char(string="Inventario", default="---", tracking=True)

    owner = fields.Many2one('res.partner', ondelete="cascade", string='Propietario',tracking=True)
    assigned = fields.Many2one('res.partner', ondelete="cascade", string='Asignado', tracking=True)
    system = fields.Many2one('cmdb.system', ondelete="cascade", string='Sistema', domain=[('active', '=', True)], tracking=True)

    status = fields.Many2one('cmdb.asset.status', ondelete="cascade", string='Estado', required=True, domain=[('active', '=', True)], tracking=True)
    installed = fields.Date("Fecha de instalacion o adquisicion", )
    active = fields.Boolean(default=True, string='Activo', tracking=True)


