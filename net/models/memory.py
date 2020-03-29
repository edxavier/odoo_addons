# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Memory(models.Model):
    _name = 'net.memory'
    _description = 'Entrada historial de memoria'

    def compute_usage(self):
        pass

    total = fields.Float(default=0, string='Total')
    free = fields.Float(default=0, string='Libre')
    usage = fields.Float(default=0, string='Uso')
    buffered = fields.Float(default=0, string='Buffer')
    shared = fields.Float(default=0, string='Shared')
    cached = fields.Float(default=0, string='Cached')
    avialable = fields.Float(default=0, string='Disponible')

    #usage_percent = fields.Float(default=0, compute=compute_usage)
    
    host_id = fields.Many2one('net.host', required=True, ondelete="cascade", string='Host')

