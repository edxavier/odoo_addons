# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SoftRunning(models.Model):
    _name = 'net.soft'
    _description = 'Entrada Software ejecuntandose'
    
    host_id = fields.Many2one('net.host', required=True, ondelete="cascade", string='Host')
    
    pid         = fields.Integer() 
    name        = fields.Char(string='Proceso')
    proc_type   = fields.Char(string='Tipo')
    status      = fields.Char()
    cpu         = fields.Float()
    mem         = fields.Float(string='Memoria')
    cpu_perc    = fields.Float(string='CPU')
