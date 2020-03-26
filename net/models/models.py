# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Host(models.Model):
    _name = 'net.host'
    _description = 'Entrada para un host'

    name = fields.Char(string="Nombre", required=True, help='Nombre o clasificacion del equipo')
    ip = fields.Char(string="Direccion IPv4", required=True, index=True)
    hostname = fields.Char(string="Hostname")
    device_type = fields.Selection(string='Tipo equipo', selection=[('server', 'Servidor'), ('workstation', 'Workstation'), ('other', 'Otro')])
    device_os = fields.Selection(string='S. operativo', selection=[('linux', 'Linux'), ('win', 'Windows'), ('other', 'Otro')])
    device_system = fields.Selection(string="Sistema", selection=[('aircon', 'Aircon'), ('sdc', 'SDC'), ('radar', 'Radar'), ('none', 'Ninguno')], default='none')
    is_up = fields.Boolean(default=False, string="Conexion")
    mem_usage = fields.Float(default=0, string="Uso RAM")
    cpu_usage = fields.Float(default=0, string="Uso CPU")
    cpu_load = fields.Float(default=0, string="Carga CPU")
    processes = fields.Float(default=0, string="Procesos")
    host_datetime = fields.Char(string="Fecha")
    uptime = fields.Char(string="Uptime")
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
