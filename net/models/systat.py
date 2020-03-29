# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SyStats(models.Model):
    _name = 'net.systat'
    _description = 'Entrada historial de memoria'

    host_id = fields.Many2one('net.host', required=True, ondelete="cascade", string='Host')

    @api.depends('raw_user', 'raw_nice', 'raw_idle', 'raw_io_wait', 'raw_kernel')
    def compute_raw_total(self):
        for rec in self:
            rec.raw_total = rec.raw_user + rec.raw_nice + rec.raw_idle + rec.raw_io_wait + rec.raw_kernel

    raw_user = fields.Float(default=0, string='Raw User')
    raw_nice = fields.Float(default=0, string='Raw Nice')
    raw_idle = fields.Float(default=0, string='Raw Idle')
    raw_io_wait = fields.Float(default=0, string='Raw IO wait')
    raw_kernel = fields.Float(default=0, string='Raw Kernel')
    raw_io_send = fields.Float(default=0, string='Raw IO sent')
    raw_io_received = fields.Float(default=0, string='Raw Io received')
    raw_interrupts = fields.Float(default=0, string='Raw Interrupts')
    raw_context_sw = fields.Float(default=0, string='Raw Context switchs')

    cpu_load = fields.Float(default=0, string='Carga cpu')

    raw_total = fields.Float(default=0, compute='compute_raw_total', store=True)
    cpu_usage = fields.Float(default=0)

    @api.model
    def create(self, vals):
        current = super(SyStats, self).create(vals)
        print("CCREATE------------------------------------------------**********************************")
        #Obtener el ultimo historial para el host seleccionado que no sea el que acabamos de guardar
        # o bien podemos hacer esta consulta antes de guardar el historial actual
        last_rec = self.env['net.systat'].search([('id','!=', current.id), ('host_id','=', vals['host_id'])], order = 'create_date desc',  limit=1) 
        lr = last_rec
        if lr.raw_total > 0:
            #print(current.create_date)
            delta_total =  current.raw_total - lr.raw_total
            delta_idle = current.raw_idle - lr.raw_idle
            delta_io_wait =current.raw_io_wait - lr.raw_io_wait
            delta_user =current.raw_user - lr.raw_user
            if delta_total > 0:
                current.cpu_usage = 100 - ((delta_idle / delta_total) * 100)
            
        return current
    