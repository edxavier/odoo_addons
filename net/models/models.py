# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Host(models.Model):
    _name = 'net.host'
    _description = 'Entrada para un host'

    def memory_history_resume(self):
        self.mem_hist_count = self.env['net.memory'].search_count([('host_id','=', self.id)])

    def systat_history_resume(self):
        self.sys_hist_count = self.env['net.systat'].search_count([('host_id','=', self.id)])


    mem_hist_count = fields.Integer("Historial memmoria", compute='memory_history_resume', store=False)
    sys_hist_count = fields.Integer("Historial rendimiento", compute='systat_history_resume', store=False)

    name = fields.Char(string="Nombre", required=True, help='Nombre o clasificacion del equipo')
    ip = fields.Char(string="Direccion IPv4", required=True, index=True)
    hostname = fields.Char(string="Hostname")
    device_type = fields.Selection(string='Tipo equipo', selection=[('server', 'Servidor'), ('workstation', 'Workstation'), ('other', 'Otro')], default='workstation')
    device_os = fields.Selection(string='S. operativo', selection=[('linux', 'Linux'), ('win', 'Windows'), ('other', 'Otro')], default='linux')
    device_system = fields.Selection(string="Sistema", selection=[('aircon', 'Aircon'), ('sdc', 'SDC'), ('radar', 'Radar'), ('none', 'Ninguno')], default='none')
    is_up = fields.Boolean(default=False, string="Conexion")
    mem_usage = fields.Float(default=0, string="Uso RAM")
    cpu_usage = fields.Float(default=0, string="Uso CPU")
    cpu_load = fields.Float(default=0, string="Carga CPU")
    processes = fields.Float(default=0, string="Procesos")
    host_datetime = fields.Char(string="Fecha")
    uptime = fields.Char(string="Uptime")

    memory_hist = fields.One2many('net.memory', 'host_id', string='Hostorial de memeoria')
    systat_hist = fields.One2many('net.systat', 'host_id', string='Historial de sistema')

    interfaces = fields.One2many('net.interface', 'host_id', string='Interfaces')
    storages = fields.One2many('net.storage', 'host_id', string='Almacenamiento')
    processes_running = fields.One2many('net.soft', 'host_id', string='Procesos')

    def open_mem_history(self):
        """return {
            'name':'Historial memoria',
            'view_mode':'tree,graph,form',
            'res_model':'net.memory',
            'type':'ir.actions.act_window',
            'domain':[('host_id','=', self.id)],
        }"""
        return {
            'type': 'ir.actions.client',
            'name':'Detailed Dashboard',
            'tag':'net_detail_dash',
            'target':'new',
            'context':{
                'host_id':self.id,
                'host_name':self.name,
            }
        }

    @api.model
    def get_user_employee_details(self):
        return {'test':22}