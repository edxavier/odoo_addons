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
            if rec.asset_type.name:
                rec.name = f"{rec.asset_type.name} [{rec.serie}]"
            else:
                rec.name = f"{rec.serie}"
            
    name = fields.Char(string="Titulo", compute='_compute_name', default='Nuevo')
    asset_type = fields.Many2one('cmdb.asset.type', ondelete="cascade", string='Tipo', required=True, domain=[('active', '=', True)], tracking=True)
    serie = fields.Char(string="Serie", help='Numero serie del activo', tracking=True, required=True)
    manufacturer = fields.Many2one('cmdb.manufacturer', ondelete="cascade", string='Marca', domain=[('active', '=', True)], tracking=True)
    model = fields.Many2one('cmdb.model', ondelete="cascade", string='Modelo', tracking=True)
    inventory = fields.Char(string="Inventario", default="---", tracking=True)
    location = fields.Char(string="Ubicacion", required=True, tracking=True)
    
    owner = fields.Many2one('res.partner', ondelete="cascade", string='Propietario',tracking=True, domain=[('is_company', '=', True)],)
    assigned = fields.Many2one('res.partner', ondelete="cascade", string='Asignado a', tracking=True, domain=[('is_company', '=', False)],)
    
    state = fields.Selection([('good', 'Bueno'), ('degraded', 'Degradado'), ('fail', 'Fallo'), ('stored', 'Almacenado'), ('discharged', 'Dado de baja')], required=True, string='Estado', default="good", tracking=True)
    active = fields.Boolean(default=True, string='Activo', tracking=True)
    item_id = fields.Many2one('cmdb.item', ondelete="cascade", string='Item asociado')



