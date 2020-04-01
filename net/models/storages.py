# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Storage(models.Model):
    _name = 'net.storage'
    _description = 'Entrada Almacenamiento'

    @api.depends('description')
    def compute_name(self):
        for rec in self:
            rec.name = rec.description
    
    @api.depends('used', 'size')
    def compute_used_percent(self):
        print('*******************COMPUTE PERC')
        for rec in self:
            if rec.size > 0:
                rec.perc_used = (rec.used / rec.size) * 100

    host_id = fields.Many2one('net.host', required=True, ondelete="cascade", string='Host')
    name = fields.Char(compute='compute_name', store=True)
    
    perc_used = fields.Float(compute='compute_used_percent', store=True, default=0)

    dev_index        = fields.Integer()
    dev_type        = fields.Char(string='Tipo')
    description        = fields.Char(string='Descripcion')
    alloc_units        = fields.Float()
    size        = fields.Float()
    used        = fields.Float()
    alloc_fails        = fields.Float()