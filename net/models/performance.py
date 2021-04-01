from odoo import models, fields, api
from datetime import datetime, timedelta

class SyStats(models.Model):
    _name = 'net.host.performance'
    _description = 'Entrada historial de rendimiento'
    _order = "create_date desc"

    host_id = fields.Many2one('net.host', required=True, ondelete="cascade", string='Host')

    cpu_user = fields.Float(default=0, string='Cpu usuario')
    cpu_io = fields.Float(default=0, string='Cpu IO wait')
    cpu_used = fields.Float(default=0, string='Uso Cpu')
    cpu_load = fields.Float(default=0, string='Carga cpu')

    plist_s = fields.Float(default=0, string='Lista de procesos')
    run_q = fields.Float(default=0, string='Cola de ejecucion')
    processes = fields.Float(default=0, string='Procesos')

    uptime = fields.Char(string="Uptime")


    interrupts = fields.Float(default=0, string='Interrupciones/s')
    context_sw = fields.Float(default=0, string='Cambio contexto/s')

    io_send = fields.Float(default=0, string='Bloques/s escritos')
    io_received = fields.Float(default=0, string='Bloques/s leidos')

    ram_mb = fields.Float(default=0, string='Mem total MB')
    ram_free_mb = fields.Float(default=0, string='Mem libre MB')
    ram_avialable_mb = fields.Float(default=0, string='Mem disponible MB')

    ram_free_p = fields.Float(default=0, string='Mem libre %')
    ram_usage_p = fields.Float(default=0, string='Mem usada %')
    ram_buffered_p = fields.Float(default=0, string='Buffer %')
    ram_shared_p = fields.Float(default=0, string='Shared %')
    ram_cached_p = fields.Float(default=0, string='Cached %')
    ram_avialable_p = fields.Float(default=0, string='Mem disponible %')


    @api.model
    def get_perfomance_resume(self):
        hosts_ids = self.env['net.host'].search([('is_up', '=', True)], order='name')
        mem_history_ds = []
        cpu_load_history_ds = []
        cpu_usage_history_ds = []
        bar_ds = []
        cpu_performance_bar_ds = []
    
        processes_bar_ds = []



        used_serie      = { 'type':'bar', 'x':[], 'y':[], 'name': 'Uso real', 'marker':{'color': "#e53935"}}
        cached_serie    = { 'type':'bar', 'x':[], 'y':[], 'name': 'Cached', 'marker':{'color': "#ffca28"}}
        shared_serie    = { 'type':'bar', 'x':[], 'y':[], 'name': 'Shared', 'marker':{'color': "#ffa726"}}
        buffered_serie  = { 'type':'bar', 'x':[], 'y':[], 'name': 'Buffered', 'marker':{'color': "#ffee58"}}
        free_serie      = { 'type':'bar', 'x':[], 'y':[], 'name': 'Free', 'marker':{'color': "#43a047"}}

        cpu_load_bar_serie  = { 'type':'bar', 'x':[], 'y':[], 'name': 'Carga cpu', 'marker':{'color': "#e53935"}}
        cpu_usage_bar_serie = { 'type':'bar', 'x':[], 'y':[], 'name': 'Uso cpu', 'marker':{'color': "#ffca28"}}

        procs_bar_serie = { 'type':'bar', 'x':[], 'y':[], 'name': 'Uso cpu', 'marker':{'color': "#ffa726"}}

        date_limit = datetime.today() - timedelta(hours=36)

        for h in hosts_ids:
            mem_usage_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': h.name, 'line':{'shape': 'spline', 'smoothing':0.8} }
            cpu_load_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': h.name, 'line':{'shape': 'spline', 'smoothing':0.8} }
            cpu_usage_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': h.name, 'line':{'shape': 'spline', 'smoothing':0.8} }

            hist = self.env['net.host.performance'].search([('host_id', '=', h.id), ('create_date', '>=', date_limit)], order='create_date desc')

            lastest_hist = self.env['net.host.performance'].search([('host_id', '=', h.id)], limit=1, order='create_date desc')

            for i in hist:
                mem_usage_serie['x'].append(i.create_date)
                mem_usage_serie['y'].append(i.ram_usage_p)

                cpu_load_serie['x'].append(i.create_date)
                cpu_load_serie['y'].append(i.cpu_load)

                cpu_usage_serie['x'].append(i.create_date)
                cpu_usage_serie['y'].append(i.cpu_used)

            mem_history_ds.append(mem_usage_serie)
            cpu_load_history_ds.append(cpu_load_serie)
            cpu_usage_history_ds.append(cpu_usage_serie)

            if lastest_hist:
                #Barchar series
                used_serie['x'].append(h.name)
                cached_serie['x'].append(h.name)
                shared_serie['x'].append(h.name)
                buffered_serie['x'].append(h.name)
                free_serie['x'].append(h.name)

                cpu_load_bar_serie['x'].append(h.name)
                cpu_usage_bar_serie['x'].append(h.name)
                procs_bar_serie['x'].append(h.name)

                used_serie['y'].append((lastest_hist.ram_usage_p)) 
                cached_serie['y'].append((lastest_hist.ram_cached_p)) 
                shared_serie['y'].append((lastest_hist.ram_shared_p)) 
                buffered_serie['y'].append((lastest_hist.ram_buffered_p)) 
                free_serie['y'].append((lastest_hist.ram_free_p)) 
                
                cpu_load_bar_serie['y'].append(lastest_hist.cpu_load)
                cpu_usage_bar_serie['y'].append(lastest_hist.cpu_used)
                procs_bar_serie['y'].append(lastest_hist.processes)



        bar_ds.append(used_serie)
        bar_ds.append(buffered_serie)
        bar_ds.append(cached_serie)
        bar_ds.append(shared_serie)
        bar_ds.append(free_serie)

        cpu_performance_bar_ds.append(cpu_usage_bar_serie)
        cpu_performance_bar_ds.append(cpu_load_bar_serie)
        processes_bar_ds.append(procs_bar_serie)
        #cpu_load_bar_ds.append(cpu_usage_bar_serie)

        return {
            'mem_history_ds': mem_history_ds, 
            'mem_bar_ds': bar_ds, 
            'cpu_load_history_ds':cpu_load_history_ds, 
            'cpu_usage_history_ds':cpu_usage_history_ds,
            'cpu_performance_bar_ds': cpu_performance_bar_ds,
            'processes_bar_ds':processes_bar_ds
        }

    @api.model
    def get_perfomance_details(self, host_id):
        mem_history_ds = []
        cpu_load_history_ds = []
        cpu_usage_history_ds = []
        
        cpu_ctx_sw_int = []
        cpu_io_ds = []

        processes_ds = []

        mem_pie_ds = []
        cpu_pie_ds = []
        mem_pie_serie   = { 
            'type':'pie', 'values':[], 'labels':['Uso','Cached','Shared','Buffered','Free',],
             'marker': {'colors':['#e53935','#ffca28','#ffa726','#ffee58','#43a047',]},
        }
        cpu_pie_serie   = { 
            #'type':'pie', 'values':[], 'labels':['Usuario','IO wait','Kernel','Sof IRQ','Hard Interruptions','IDLE'], 
            'type':'pie', 'values':[], 'labels':['Usuario','IO wait','IDLE'], 
            #'marker': {'colors':['#e53935','#ffca28','#ffa726','#ffee58','#bdbdbd','#43a047',]},
            'marker': {'colors':['#e53935','#ffca28', '#43a047',]},
        }

        mem_used_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Usado', 'line':{'shape': 'spline', 'smoothing':0.8} }

        processes_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Procesos', 'line':{'shape': 'spline', 'smoothing':0.8} }
        plist_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Lista tareas', 'line':{'shape': 'spline', 'smoothing':0.8} }
        runq_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Cola de ejecucion', 'line':{'shape': 'spline', 'smoothing':0.8} }
        
        cpu_load_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Carga de CPU', 'line':{'shape': 'spline', 'smoothing':0.8} }
        
        cpu_usage_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Uso de CPU', 'line':{'shape': 'spline', 'smoothing':0.8} }

        cpu_ctx_sw = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Cambios de contexto', 'line':{'shape': 'spline', 'smoothing':0.8} }
        cpu_interrupts = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Interrupciones', 'line':{'shape': 'spline', 'smoothing':0.8} }

        io_send_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Bloques escritos', 'line':{'shape': 'spline', 'smoothing':0.8} }
        io_received_serie = { 'type':'scatter', 'x':[], 'y':[], 'name': 'Bloques leidos', 'line':{'shape': 'spline', 'smoothing':0.8} }

        date_limit = datetime.today() - timedelta(days=15)
        hist = self.env['net.host.performance'].search([('host_id', '=', host_id), ('create_date', '>=', date_limit)], order='create_date desc')

        lastest_hist = self.env['net.host.performance'].search([('host_id', '=', host_id)], limit=1, order='create_date desc')

        if lastest_hist:
            mem_pie_serie['values'].append((lastest_hist.ram_usage_p)) #/lastest_hist.total) * 100
            mem_pie_serie['values'].append((lastest_hist.ram_cached_p)) #/lastest_hist.total) * 100
            mem_pie_serie['values'].append((lastest_hist.ram_shared_p)) #/lastest_hist.total) * 100
            mem_pie_serie['values'].append((lastest_hist.ram_buffered_p)) #/lastest_hist.total) * 100
            mem_pie_serie['values'].append((lastest_hist.ram_free_p)) #/lastest_hist.total) * 100
        
            cpu_pie_serie['values'].append((lastest_hist.cpu_user)) #/lastest_hist.total) * 100
            cpu_pie_serie['values'].append((lastest_hist.cpu_io)) #/lastest_hist.total) * 100
            cpu_pie_serie['values'].append(100-(lastest_hist.cpu_used)) #/last_stat_hist.total) * 100
        
        mem_pie_ds.append(mem_pie_serie)
        cpu_pie_ds.append(cpu_pie_serie)


        # Graficos de linea
        for i in hist:
            #mem_total_serie['x'].append(i.create_date)
            #mem_total_serie['y'].append(i.total)

            mem_used_serie['x'].append(i.create_date)
            mem_used_serie['y'].append(i.ram_usage_p)

            #mem_buffered_serie['x'].append(i.create_date)
            #mem_buffered_serie['y'].append(i.buffered)

            #mem_cached_serie['x'].append(i.create_date)
            #mem_cached_serie['y'].append(i.cached)

            #mem_shared_serie['x'].append(i.create_date)
            #mem_shared_serie['y'].append(i.shared)

            #mem_avialable_serie['x'].append(i.create_date)
            #mem_avialable_serie['y'].append(i.avialable)
        
            io_send_serie['x'].append(i.create_date)
            io_send_serie['y'].append(i.io_send)

            io_received_serie['x'].append(i.create_date)
            io_received_serie['y'].append(i.io_received)

            cpu_load_serie['x'].append(i.create_date)
            cpu_load_serie['y'].append(i.cpu_load)

            cpu_usage_serie['x'].append(i.create_date)
            cpu_usage_serie['y'].append(i.cpu_used)

            cpu_ctx_sw['x'].append(i.create_date)
            cpu_ctx_sw['y'].append(i.context_sw)

            cpu_interrupts['x'].append(i.create_date)
            cpu_interrupts['y'].append(i.interrupts)

            processes_serie['x'].append(i.create_date)
            processes_serie['y'].append(i.processes)

            plist_serie['x'].append(i.create_date)
            plist_serie['y'].append(i.plist_s)

            runq_serie['x'].append(i.create_date)
            runq_serie['y'].append(i.run_q)


            # CPU USAGE
            """cpu_io_serie['x'].append(i.create_date)
            cpu_io_serie['y'].append(i.cpu_io_wait)

            cpu_user_serie['x'].append(i.create_date)
            cpu_user_serie['y'].append(i.cpu_user)

            cpu_kernel_serie['x'].append(i.create_date)
            cpu_kernel_serie['y'].append(i.cpu_kernel)

            cpu_irq_serie['x'].append(i.create_date)
            cpu_irq_serie['y'].append(i.cpu_soft_irq)

            cpu_ints_serie['x'].append(i.create_date)
            cpu_ints_serie['y'].append(i.cpu_hard_int)
            """


        #mem_history_ds.append(mem_total_serie)
        mem_history_ds.append(mem_used_serie)
        #mem_history_ds.append(mem_buffered_serie)
        #mem_history_ds.append(mem_cached_serie)
        #mem_history_ds.append(mem_shared_serie)
        #mem_history_ds.append(mem_avialable_serie)

        cpu_load_history_ds.append(cpu_load_serie)

        cpu_usage_history_ds.append(cpu_usage_serie)
        #cpu_usage_history_ds.append(cpu_user_serie)
        #cpu_usage_history_ds.append(cpu_io_serie)
        #cpu_usage_history_ds.append(cpu_kernel_serie)
        #cpu_usage_history_ds.append(cpu_irq_serie)
        #cpu_usage_history_ds.append(cpu_ints_serie)

        cpu_io_ds.append(io_send_serie)
        cpu_io_ds.append(io_received_serie)

        processes_ds.append(processes_serie)
        processes_ds.append(plist_serie)
        processes_ds.append(runq_serie)

        cpu_ctx_sw_int.append(cpu_interrupts)
        cpu_ctx_sw_int.append(cpu_ctx_sw)

        return {
            'cpu_io_ds':cpu_io_ds,
            'processes_ds':processes_ds,
            'cpu_ctx_sw_int':cpu_ctx_sw_int,
            'cpu_pie_ds': cpu_pie_ds, 'mem_bar_ds': mem_pie_ds,
            'mem_history_ds': mem_history_ds, 
            'cpu_load_history_ds':cpu_load_history_ds, 
            'cpu_usage_history_ds':cpu_usage_history_ds}
