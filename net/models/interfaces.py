# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Storage(models.Model):
    _name = 'net.interface'
    _description = 'Entrada Interface'

    @api.depends('description')
    def compute_name(self):
        for rec in self:
            rec.name = rec.description

    host_id = fields.Many2one('net.host', required=True, ondelete="cascade", string='Host')

    name = fields.Char(compute='compute_name', store=True)
    if_index    = fields.Float(default=0)
    in_octets   = fields.Float(default=0)
    in_errors   = fields.Float(default=0)
    out_octets  = fields.Float(default=0)
    out_errors  = fields.Float(default=0)
    description = fields.Char(default='---')
    if_type     = fields.Char(default='---')
    mac         = fields.Char(default='---')
    oper_stat   = fields.Char(default='---', string='Estado')