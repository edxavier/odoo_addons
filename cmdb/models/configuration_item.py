# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Item(models.Model):
    _name = 'cmdb.item'
    _description = 'Item de configuracion'
    _inherit = ['mail.thread']

    @api.onchange('system')
    def systemOnchange(self):
        for rec in self:
            rec.subsystem = None
            return {'domain': {'subsystem': [('system', '=', rec.system.id)]}}

    """@api.onchange('manufacturer')
    def manufacturerOnchange(self):
        for rec in self:
            rec.model = None
            return {'domain': {'model': [('manufacturer', '=', rec.manufacturer.id)]}}
    """

    sequence = fields.Char(string='Codigo item', required=True, copy=False, readonly=True, index=True, default='Nuevo')
    name = fields.Char(string="Nombre", help='Nombre o clasificacion del equipo', required=True,)
    system = fields.Many2one('cmdb.system', ondelete="cascade", string='Sistema', required=True, domain=[('active', '=', True)])
    subsystem = fields.Many2one('cmdb.subsystem', ondelete="cascade", string='Subsistema', required=True, domain=[('active', '=', True)])
    state = fields.Selection([('ok', 'Operando'), ('degraded', 'Degradado'), ('fail', 'Fallo'), ('inactive', 'Inactivo')], required=True, string='Estado', default="ok", tracking=True)
    active = fields.Boolean(default=True, string='Activo')
    related_assets =  fields.One2many('cmdb.asset', 'item_id', string=' Activos asociados', ondelete='set null')
    
    #item_type = fields.Many2one('cmdb.item.type', ondelete="cascade", string='Tipo', required=True, domain=[('active', '=', True)])
    #building = fields.Many2one('cmdb.building', ondelete="cascade", string='Edificio', domain=[('active', '=', True)])
    #office = fields.Many2one('cmdb.office', ondelete="cascade", string='Oficina', domain=[('active', '=', True)])

    #owner = fields.Many2one('res.partner', ondelete="cascade", string='Propietario')
    #responsable = fields.Many2one('res.partner', ondelete="cascade", string='Responsable')
    
    #alternative_items = fields.Many2many('cmdb.item', column1='item_id', relation="item_alternatives", column2='item_alt_id', string='Item alternativos')

    #installed = fields.Date("Fecha de instalacion o adquisicion", )


    @api.model
    def create(self, vals):
        if vals.get('sequence', 'Nuevo') == 'Nuevo':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('cmdb.item.sequence') or 'Nuevo'
        return super(Item, self).create(vals)
