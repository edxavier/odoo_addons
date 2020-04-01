# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SyStats(models.Model):
    _name = 'net.systat'
    _description = 'Entrada historial de memoria'
    _order = "create_date desc"

    host_id = fields.Many2one('net.host', required=True, ondelete="cascade", string='Host')

    @api.depends('raw_user', 'raw_nice', 'raw_idle', 'raw_io_wait', 'raw_kernel')
    def compute_raw_total(self):
        for rec in self:
            rec.raw_total = rec.raw_user + rec.raw_nice + rec.raw_idle + rec.raw_io_wait + rec.raw_kernel + rec.raw_soft_irq + rec.raw_cpu_interrupt

    raw_user = fields.Float(default=0, string='Raw User')
    raw_nice = fields.Float(default=0, string='Raw Nice')
    raw_idle = fields.Float(default=0, string='Raw Idle')
    raw_io_wait = fields.Float(default=0, string='Raw IO wait')
    raw_kernel = fields.Float(default=0, string='Raw Kersnel')
    raw_io_send = fields.Float(default=0, string='Raw IO sent')
    raw_io_received = fields.Float(default=0, string='Raw Io received')
    raw_interrupts = fields.Float(default=0, string='Raw Interrupts')
    raw_context_sw = fields.Float(default=0, string='Raw Context switchs')

    raw_soft_irq = fields.Float(default=0, string='Raw Sof IRQ')
    raw_cpu_interrupt = fields.Float(default=0, string='Raw CPU Interrups')

    cpu_load = fields.Float(default=0, string='Carga cpu')

    raw_total = fields.Float(default=0, compute='compute_raw_total', store=True)
    
    cpu_usage = fields.Float(default=0, string='Uso cpu')
    cpu_io_wait = fields.Float(default=0, string='IO wait')
    cpu_user = fields.Float(default=0, string='Usuario')

    cpu_kernel = fields.Float(default=0, string='Kernel')
    cpu_soft_irq = fields.Float(default=0, string='Int. Soft')
    cpu_hard_int = fields.Float(default=0, string='Int. Hard')

    io_send = fields.Float(default=0, string='Bloques/s escritos')
    io_received = fields.Float(default=0, string='Bloques/s leidos')
    context_sw = fields.Float(default=0, string='Cambio contexto/s')
    interrupts = fields.Float(default=0, string='Interrupciones/s')

    @api.model
    def create(self, vals):
        last_rec = self.env['net.systat'].search([('host_id','=', vals['host_id'])], order = 'create_date desc',  limit=1) 
        current = super(SyStats, self).create(vals)
        #Obtener el ultimo historial para el host seleccionado que no sea el que acabamos de guardar
        # o bien podemos hacer esta consulta antes de guardar el historial actual
        #last_rec = self.env['net.systat'].search([('id','!=', current.id), ('host_id','=', vals['host_id'])], order = 'create_date desc',  limit=1) 
        host = self.env['net.host'].search([('id','=', vals['host_id'])], order = 'create_date desc',  limit=1) 
        
        lr = last_rec
        if lr.raw_total > 0:
            #print(current.create_date)
            # Calcular la diferencia de valores entre el nuevo registro y el registro anterior
            #current.raw_total         = self.check_int32_limit(current.raw_total,lr.raw_total)
            #print(current.host_id.name)
            #print("CURRENT RAW IDLE: " + str(current.raw_idle))
            #print("LAST RAW IDLE: " + str(lr.raw_idle))
            
            """
            #print("NEW CURRENT RAW IDLE: " + str(current.raw_idle))
            """
            
            if current.raw_total > lr.raw_total:
                #print("CURRENT RAW TOTAL GREATER THAN**************************************")
                delta_total = current.raw_total - lr.raw_total
                #delta_total = current.raw_total - lr.raw_total        
                delta_idle = current.raw_idle - lr.raw_idle
                delta_io_wait =current.raw_io_wait - lr.raw_io_wait
                delta_user =current.raw_user - lr.raw_user
                delta_soft =current.raw_soft_irq - lr.raw_soft_irq
                delta_hard =current.raw_cpu_interrupt - lr.raw_cpu_interrupt
                delta_kernel = current.raw_kernel - lr.raw_kernel
            else:
                #print("CURRENT RAW TOTAL LESS THAN")
                delta_total = current.raw_total
                delta_idle = current.raw_idle 
                delta_io_wait =current.raw_io_wait 
                delta_user =current.raw_user
                delta_soft =current.raw_soft_irq
                delta_hard =current.raw_cpu_interrupt 
                delta_kernel = current.raw_kernel 


            
            """current.raw_idle          = self.check_int32_limit(current.raw_idle, lr.raw_idle)
            current.raw_io_wait       = self.check_int32_limit(current.raw_io_wait,lr.raw_io_wait)
            current.raw_user          = self.check_int32_limit(current.raw_user,lr.raw_user)
            current.raw_soft_irq      = self.check_int32_limit(current.raw_soft_irq,lr.raw_soft_irq)
            current.raw_cpu_interrupt = self.check_int32_limit(current.raw_cpu_interrupt,lr.raw_cpu_interrupt)
            current.raw_kernel        = self.check_int32_limit(current.raw_kernel,lr.raw_kernel)
            
            current.raw_io_send       = self.check_int32_limit(current.raw_io_send,lr.raw_io_send)
            current.raw_io_received   = self.check_int32_limit(current.raw_io_received,lr.raw_io_received)
            current.raw_context_sw    = self.check_int32_limit(current.raw_context_sw,lr.raw_context_sw)
            current.raw_interrupts    = self.check_int32_limit(current.raw_interrupts,lr.raw_interrupts)
            """
            
        
            if delta_total > 0:
                current.cpu_usage = 100 - ((delta_idle / delta_total) * 100)
                current.cpu_io_wait = ((delta_io_wait / delta_total) * 100)
                current.cpu_user = ((delta_user / delta_total) * 100)
                current.cpu_kernel = ((delta_kernel / delta_total) * 100)
                current.cpu_soft_irq = ((delta_soft / delta_total) * 100)
                current.cpu_hard_int = ((delta_hard / delta_total) * 100)

                host.cpu_usage = current.cpu_usage

            delta_time = current.create_date - lr.create_date
            seconds = delta_time.total_seconds()
            """ Si el registro actual es menor que el anterior, no hacer los calculos y dejar en 0"""
            if current.raw_io_send >= lr.raw_io_send:
                delta_io_send = current.raw_io_send - lr.raw_io_send
                current.io_send = delta_io_send / seconds
                #print(host.name +" IO SEND "+ str(current.io_send))
                #print( )

            
            if current.raw_io_received >= lr.raw_io_received:
                delta_io_received  = current.raw_io_received - lr.raw_io_received
                current.io_received = delta_io_received / seconds
            
            if current.raw_context_sw >= lr.raw_context_sw:
                delta_context_sw = current.raw_context_sw - lr.raw_context_sw
                current.context_sw = delta_context_sw / seconds
            
            if current.raw_interrupts >= lr.raw_interrupts:
                delta_interrupts = current.raw_interrupts - lr.raw_interrupts
                current.interrupts = delta_interrupts / seconds
            
                
        return current

    def check_int32_limit(self, current, last):
        # When the SNMP counter reaches 4,294,967,295, it will rollover and reset to ZERO.
        # If this happens, we want to make sure we don't output a negative bps
        if current < last:
            # If we reset to 0, add the max value of the octets counter
            current += 4294967295
            ## Max numero entero de 32 bits 4294967295
        return current