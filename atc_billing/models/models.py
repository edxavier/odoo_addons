# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime 
from pytz import timezone


FLIGHT_TYPES = [('S', 'Programado'), ('N', 'No programado'), 
                ('G', 'Aviación general'), ('M', 'Militar'), 
                ('X', 'Otro')]

WAKE_TURBULENCES = [('S', 'Superpesada'), ('H', 'Pesada'), 
                 ('M', 'Media'), ('L', 'Ligera')]

class FlightPlan(models.Model):
    _name = 'atc_billing.flightplan'
    _description = 'Plan de vuelo'
    _rec_name = 'call_sign'
    
    @api.depends('call_sign')
    def compute_name(self):
        for rec in self:
            rec.name = rec.call_sign

    @api.depends('initial_time',)
    def compute_date_format(self):
        for rec in self:
            rec.utc_date_str = rec.initial_time.strftime("%d-%m-%Y %H:%M")

    @api.depends('initial_time',)
    def compute_local_date_format(self):
        for rec in self:
            obj = rec.initial_time.astimezone(timezone('America/Managua'))
            rec.local_date_str = obj.strftime("%d-%m-%Y %H:%M")

    name = fields.Char(compute='compute_name', store=True)
    secuence = fields.Integer(default=-1)
    call_sign = fields.Char()
    register = fields.Char(string="Resgistro")
    flight_type = fields.Selection(FLIGHT_TYPES, string='Tipo de vuelo')
    origin = fields.Char(string="Origen")
    #sid = fields.Char(string="SID")
    aircraft_type = fields.Char(string='Tipo de aeronave')
    #speed = fields.Integer(string='Velocidad')
    destination = fields.Char(string="Destino")
    #start = fields.Char(string="Inicio")
    arrival_time = fields.Char(string="Fin vuelo")
    #rfl = fields.Char(string="RFL")
    initial_time = fields.Datetime(string="Inicio de vuelo")
    #ssr_code = fields.Char(string="Codigo SSR")
    #flight_duration = fields.Char(string="Duracion de vuelo")
    #distance = fields.Integer(string='Distancia')
    #wake_turbulence = fields.Selection(WAKE_TURBULENCES, string='Tipo de Estela')
    #nav_equipment = fields.Char(string="Equipo de navegacion")
    #operator = fields.Char(string="Operador")
    
    takeoff_time = fields.Char(string="Hora de despegue")
    landing_time = fields.Char(string="Hora de aterrizaje")
    utc_date_str = fields.Char(string="Inicio vuelo (UTC)",  compute='compute_date_format', store=False)
    local_date_str = fields.Char(string="Inicio vuelo (hora local)",  compute='compute_local_date_format', store=False)


    """@api.model
    def create(self, vals):
        if vals.get('origin') == 'MNMG':
            date_time_obj = datetime.strptime(vals.get('initial_time'), '%Y-%m-%d %H:%M:%S')            
            time = date_time_obj.strftime("%H:%M:%S")
            hour = vals.get('initial_time').split(' ')[1].split(':')
            vals['takeoff_time'] = hour[0]+ hour[1]

        if vals.get('destination') == 'MNMG':
            vals['landing_time'] = vals.get('arrival_time')

        return super(FlightPlan, self).create(vals)
    """
