# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Memory(models.Model):
    _name = 'net.memory'
    _description = 'Entrada historial de memoria'

    @api.depends('total', 'usage')
    def compute_usage_percent(self):
        for rec in self:
            if rec.total > 0:
                rec.usage_percent = (rec.usage/rec.total) * 100

    # unidades en MB
    total = fields.Float(default=0, string='Total')
    free = fields.Float(default=0, string='Libre')
    usage = fields.Float(default=0, string='Uso')
    buffered = fields.Float(default=0, string='Buffer')
    shared = fields.Float(default=0, string='Shared')
    cached = fields.Float(default=0, string='Cached')
    avialable = fields.Float(default=0, string='Disponible')

    usage_percent = fields.Float(default=0, compute='compute_usage_percent', store=True, string='Uso')

    #usage_percent = fields.Float(default=0, compute=compute_usage)
    
    host_id = fields.Many2one('net.host', required=True, ondelete="cascade", string='Host')

    @api.model
    def get_host_details(self, host_id):
        mem_history_ds = []
        cpu_load_history_ds = []
        cpu_usage_history_ds = []
        
        cpu_ctx_sw_int = []
        cpu_io_ds = []

        mem_pie_ds = []
        cpu_pie_ds = []
        mem_pie_serie   = { 
            'type':'pie', 'values':[], 'labels':['Uso','Cached','Shared','Buffered','Free',],
             'marker': {'colors':['#e53935','#ffca28','#ffa726','#ffee58','#43a047',]},
        }
        cpu_pie_serie   = { 
            'type':'pie', 'values':[], 'labels':['Usuario','IO wait','Kernel','Sof IRQ','Hard Interruptions','IDLE'], 
             'marker': {'colors':['#e53935','#ffca28','#ffa726','#ffee58','#bdbdbd','#43a047',]},
        }

        mem_total_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Total', 'line':{'shape': 'spline', 'smoothing':0.8} }
        mem_used_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Usado', 'line':{'shape': 'spline', 'smoothing':0.8} }
        mem_buffered_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Buffered', 'line':{'shape': 'spline', 'smoothing':0.8} }
        mem_cached_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Cached', 'line':{'shape': 'spline', 'smoothing':0.8} }
        mem_shared_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Shared', 'line':{'shape': 'spline', 'smoothing':0.8} }
        mem_avialable_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Disponible', 'line':{'shape': 'spline', 'smoothing':0.8} }
        
        cpu_load_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Carga de CPU', 'line':{'shape': 'spline', 'smoothing':0.8} }
        
        cpu_usage_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Uso de CPU', 'line':{'shape': 'spline', 'smoothing':0.8} }
        cpu_user_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Usuario', 'line':{'shape': 'spline', 'smoothing':0.8} }
        cpu_io_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'IO wait', 'line':{'shape': 'spline', 'smoothing':0.8} }
        cpu_kernel_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Kernel', 'line':{'shape': 'spline', 'smoothing':0.8} }
        cpu_irq_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'IRQ', 'line':{'shape': 'spline', 'smoothing':0.8} }
        cpu_ints_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Interrupciones', 'line':{'shape': 'spline', 'smoothing':0.8} }

        cpu_ctx_sw = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Cambios de contexto', 'line':{'shape': 'spline', 'smoothing':0.8} }
        cpu_interrupts = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Interrupciones', 'line':{'shape': 'spline', 'smoothing':0.8} }

        io_send_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Bloques escritos', 'line':{'shape': 'spline', 'smoothing':0.8} }
        io_received_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Bloques leidos', 'line':{'shape': 'spline', 'smoothing':0.8} }

        
        mem_hist = self.env['net.memory'].search([('host_id', '=', host_id)], limit=1500, order='create_date desc')
        stat_hist = self.env['net.systat'].search([('host_id', '=', host_id)], limit=1500, order='create_date desc')
            
        last_mem_hist = self.env['net.memory'].search([('host_id', '=', host_id)], limit=1, order='create_date desc')
        last_stat_hist = self.env['net.systat'].search([('host_id', '=', host_id)], limit=1, order='create_date desc')
            
        for i in mem_hist:
            mem_total_serie['x'].append(i.create_date)
            mem_total_serie['y'].append(i.total)

            mem_used_serie['x'].append(i.create_date)
            mem_used_serie['y'].append(i.usage)

            mem_buffered_serie['x'].append(i.create_date)
            mem_buffered_serie['y'].append(i.buffered)

            mem_cached_serie['x'].append(i.create_date)
            mem_cached_serie['y'].append(i.cached)

            mem_shared_serie['x'].append(i.create_date)
            mem_shared_serie['y'].append(i.shared)

            mem_avialable_serie['x'].append(i.create_date)
            mem_avialable_serie['y'].append(i.avialable)
        for i in stat_hist:
            io_send_serie['x'].append(i.create_date)
            io_send_serie['y'].append(i.io_send)

            io_received_serie['x'].append(i.create_date)
            io_received_serie['y'].append(i.io_received)

            cpu_load_serie['x'].append(i.create_date)
            cpu_load_serie['y'].append(i.cpu_load)

            cpu_usage_serie['x'].append(i.create_date)
            cpu_usage_serie['y'].append(i.cpu_usage)

            cpu_ctx_sw['x'].append(i.create_date)
            cpu_ctx_sw['y'].append(i.context_sw)

            cpu_interrupts['x'].append(i.create_date)
            cpu_interrupts['y'].append(i.interrupts)

            # CPU USAGE
            cpu_io_serie['x'].append(i.create_date)
            cpu_io_serie['y'].append(i.cpu_io_wait)

            cpu_user_serie['x'].append(i.create_date)
            cpu_user_serie['y'].append(i.cpu_user)

            cpu_kernel_serie['x'].append(i.create_date)
            cpu_kernel_serie['y'].append(i.cpu_kernel)

            cpu_irq_serie['x'].append(i.create_date)
            cpu_irq_serie['y'].append(i.cpu_soft_irq)

            cpu_ints_serie['x'].append(i.create_date)
            cpu_ints_serie['y'].append(i.cpu_hard_int)


        mem_history_ds.append(mem_total_serie)
        mem_history_ds.append(mem_used_serie)
        mem_history_ds.append(mem_buffered_serie)
        mem_history_ds.append(mem_cached_serie)
        mem_history_ds.append(mem_shared_serie)
        mem_history_ds.append(mem_avialable_serie)

        cpu_load_history_ds.append(cpu_load_serie)

        cpu_usage_history_ds.append(cpu_usage_serie)
        cpu_usage_history_ds.append(cpu_user_serie)
        cpu_usage_history_ds.append(cpu_io_serie)
        cpu_usage_history_ds.append(cpu_kernel_serie)
        cpu_usage_history_ds.append(cpu_irq_serie)
        cpu_usage_history_ds.append(cpu_ints_serie)

        cpu_io_ds.append(io_send_serie)
        cpu_io_ds.append(io_received_serie)

        cpu_ctx_sw_int.append(cpu_interrupts)
        cpu_ctx_sw_int.append(cpu_ctx_sw)

        if last_mem_hist:
            mem_pie_serie['values'].append((last_mem_hist.usage)) #/last_mem_hist.total) * 100
            mem_pie_serie['values'].append((last_mem_hist.cached)) #/last_mem_hist.total) * 100
            mem_pie_serie['values'].append((last_mem_hist.shared)) #/last_mem_hist.total) * 100
            mem_pie_serie['values'].append((last_mem_hist.buffered)) #/last_mem_hist.total) * 100
            mem_pie_serie['values'].append((last_mem_hist.free)) #/last_mem_hist.total) * 100
        
        if last_stat_hist:
            cpu_pie_serie['values'].append((last_stat_hist.cpu_user)) #/last_stat_hist.total) * 100
            cpu_pie_serie['values'].append((last_stat_hist.cpu_io_wait)) #/last_stat_hist.total) * 100
            cpu_pie_serie['values'].append((last_stat_hist.cpu_kernel)) #/last_stat_hist.total) * 100
            cpu_pie_serie['values'].append((last_stat_hist.cpu_soft_irq)) #/last_stat_hist.total) * 100
            cpu_pie_serie['values'].append((last_stat_hist.cpu_hard_int)) #/last_stat_hist.total) * 100
            cpu_pie_serie['values'].append(100-(last_stat_hist.cpu_usage)) #/last_stat_hist.total) * 100
        
    
        mem_pie_ds.append(mem_pie_serie)
        cpu_pie_ds.append(cpu_pie_serie)
        
        return {
            'cpu_io_ds':cpu_io_ds,
            'cpu_ctx_sw_int':cpu_ctx_sw_int,
            'cpu_pie_ds': cpu_pie_ds, 'mem_bar_ds': mem_pie_ds,
            'mem_history_ds': mem_history_ds, 
            'cpu_load_history_ds':cpu_load_history_ds, 
            'cpu_usage_history_ds':cpu_usage_history_ds}
        

    @api.model
    def get_memory_history(self):
        hosts_ids = self.env['net.host'].search([])
        mem_history_ds = []
        cpu_load_history_ds = []
        cpu_usage_history_ds = []

        bar_ds = []

        used_serie      = { 'type':'bar', 'x':[], 'y':[], 'name': 'Uso real', 'marker':{'color': "#e53935"}}
        cached_serie    = { 'type':'bar', 'x':[], 'y':[], 'name': 'Cached', 'marker':{'color': "#ffca28"}}
        shared_serie    = { 'type':'bar', 'x':[], 'y':[], 'name': 'Shared', 'marker':{'color': "#ffa726"}}
        buffered_serie  = { 'type':'bar', 'x':[], 'y':[], 'name': 'Buffered', 'marker':{'color': "#ffee58"}}
        free_serie      = { 'type':'bar', 'x':[], 'y':[], 'name': 'Free', 'marker':{'color': "#43a047"}}
                
        for h in hosts_ids:
            plot_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': h.name, 'line':{'shape': 'spline', 'smoothing':0.8} }
            cpu_load_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': h.name, 'line':{'shape': 'spline', 'smoothing':0.8} }
            cpu_usage_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': h.name, 'line':{'shape': 'spline', 'smoothing':0.8} }

            hist = self.env['net.memory'].search([('host_id', '=', h.id)], limit=500, order='create_date desc')
            stat_hist = self.env['net.systat'].search([('host_id', '=', h.id)], limit=500, order='create_date desc')
            
            last_hist = self.env['net.memory'].search([('host_id', '=', h.id)], limit=1, order='create_date desc')
            
            for i in hist:
                plot_serie['x'].append(i.create_date)
                plot_serie['y'].append(i.usage_percent)
            for i in stat_hist:
                cpu_load_serie['x'].append(i.create_date)
                cpu_load_serie['y'].append(i.cpu_load)
                cpu_usage_serie['x'].append(i.create_date)
                cpu_usage_serie['y'].append(i.cpu_usage)

            mem_history_ds.append(plot_serie)
            cpu_load_history_ds.append(cpu_load_serie)
            cpu_usage_history_ds.append(cpu_usage_serie)

            used_serie['x'].append(h.name)
            cached_serie['x'].append(h.name)
            shared_serie['x'].append(h.name)
            buffered_serie['x'].append(h.name)
            free_serie['x'].append(h.name)
            if last_hist:
                used_serie['y'].append((last_hist.usage)) #/last_hist.total) * 100
                cached_serie['y'].append((last_hist.cached)) #/last_hist.total) * 100
                shared_serie['y'].append((last_hist.shared)) #/last_hist.total) * 100
                buffered_serie['y'].append((last_hist.buffered)) #/last_hist.total) * 100
                free_serie['y'].append((last_hist.free)) #/last_hist.total) * 100
        
        bar_ds.append(used_serie)
        bar_ds.append(buffered_serie)
        bar_ds.append(cached_serie)
        bar_ds.append(shared_serie)
        bar_ds.append(free_serie)
        
        return {'mem_history_ds': mem_history_ds, 'mem_bar_ds': bar_ds, 'cpu_load_history_ds':cpu_load_history_ds, 'cpu_usage_history_ds':cpu_usage_history_ds}
