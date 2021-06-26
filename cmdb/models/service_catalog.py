# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Service(models.Model):
    _name = 'cmdb.service'
    _description = 'Servicio'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Char(string='Codigo servicio', required=True, copy=False, readonly=True, index=True, default='Nuevo')
    name = fields.Char(string="Nombre", help='Nombre', required=True)
    description = fields.Text(string="Descripcion", help='Descripcion')
    owner = fields.Many2one('res.partner', ondelete="cascade", string='Propietario')
    responsable = fields.Many2one('res.partner', ondelete="cascade", string='Responsable')
    service_type = fields.Many2one('cmdb.service.type', ondelete="cascade", string='Tipo', required=True)
    category = fields.Selection([('intern', ' Interno'), ('extern', 'Externo')], required=True, string='Categoria')

    alternative_service = fields.Many2many('cmdb.service', column1='service_id', 
    relation="service_alternatives", column2='service_alt_id', string='Servicios alternativos')

    status = fields.Many2one('cmdb.service.status', ondelete="cascade", string='Estado', required=True)
    active = fields.Boolean(default=True, string='Activo')

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'Nuevo') == 'Nuevo':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('cmdb.service.sequence') or 'Nuevo'
        return super(Service, self).create(vals)
