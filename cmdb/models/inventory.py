# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Asset(models.Model):
    _name = 'cmdb.asset'
    _description = 'Activo'
    _inherit = ['mail.thread']


    @api.onchange('manufacturer')
    def manufacturerOnchange(self):
        for rec in self:
            rec.model = None
            return {'domain': {'model': [('manufacturer', '=', rec.manufacturer.id)]}}

    @api.onchange('building')
    def buindingOnchange(self):
        for rec in self:
            rec.office = None
            return {'domain': {'office': [('building', '=', rec.building.id)]}}

    @api.depends('asset_type', 'serie')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.asset_type.name  + '|' + rec.serie
            
    name = fields.Char(string="Titulo", compute='_compute_name', default='Nuevo')
    asset_type = fields.Many2one('cmdb.asset.type', ondelete="cascade", string='Tipo', required=True, domain=[('active', '=', True)], tracking=True)
    serie = fields.Char(string="Serie", help='Numero serie del activo', tracking=True, required=True)
    manufacturer = fields.Many2one('cmdb.manufacturer', ondelete="cascade", string='Marca', domain=[('active', '=', True)], tracking=True)
    model = fields.Many2one('cmdb.model', ondelete="cascade", string='Modelo', tracking=True)
    inventory = fields.Char(string="Inventario", default="---", tracking=True)
    
    building = fields.Many2one('cmdb.building', ondelete="cascade", string='Edificio', domain=[('active', '=', True)])
    office = fields.Many2one('cmdb.office', ondelete="cascade", string='Oficina', domain=[('active', '=', True)])
    location = fields.Char(string="Ubicacion", required=True, tracking=True)
    
    note = fields.Text(string="Nota", help='Nota')
    

    owner = fields.Many2one('res.partner', ondelete="cascade", string='Propietario',tracking=True, domain=[('is_company', '=', True)],)
    assigned = fields.Many2one('res.partner', ondelete="cascade", string='Asignado', tracking=True, domain=[('active', '=', False)],)

    status = fields.Many2one('cmdb.asset.status', ondelete="cascade", string='Estado', required=True, domain=[('active', '=', True)], tracking=True)
    active = fields.Boolean(default=True, string='Activo', tracking=True)


