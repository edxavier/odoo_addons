# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Status(models.Model):
    _name = 'maint.status'
    _description = 'Estado de mantenimiento'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    #item = fields.Many2one('maint.maintenance', ondelete="cascade", string='Pertenece a', required=True,)


class Frecuency(models.Model):
    _name = 'maint.frecuency'
    _description = 'Frecuencia de mantenimiento'

    name = fields.Char(required=True)
    days = fields.Integer(required=True, string='Frecuencia en dias')
    active = fields.Boolean(default=True)

class Maintenance(models.Model):
    _name = 'maint.maintenance'
    _description = ' Mantenimiento'

    name = fields.Char(required=True, string='Nombre')
    description = fields.Text(string='Descripcion del mantenimiento')
    affected_items = fields.Many2many('cmdb.item', string='Items afectados', domain=[('active', '=', True), ('maintainable', '=', True)])
    frecuency = fields.Many2one('maint.frecuency', ondelete="cascade", required=True, string='Frecuencia', domain=[('active', '=', True)])
    last_execution = fields.Date("Fecha de ultima ejecucion", required=True)
    active = fields.Boolean(default=True, string='Activo')

class Program(models.Model):
    _name = 'maint.program'
    _description = 'Programacion de mantenimientos'
    _rec_name = 'maintenance'

    name = fields.Char(string='Nombre', default='---')
    plan_id = fields.Many2one('maint.plan', ondelete="cascade", string='Plan', required=True,)
    maintenance = fields.Many2one('maint.maintenance', ondelete="cascade", required=True, string='Mantenimiento', domain=[('active', '=', True)])
    expected_execution = fields.Date("Programado para", required=True)
    started = fields.Date("Iniciado", required=False)
    finished = fields.Date("Programado para", required=False)
    real_execution = fields.Date("Iniciado")
    responsable = fields.Many2one('res.partner', ondelete="cascade", string='Responsable', required=True,)
    support_staff = fields.Many2many('res.partner', string='Participantes', domain=[('active', '=', True)])
    status = fields.Many2one('maint.status', ondelete="cascade", required=True, string='Estado', domain=[('active', '=', True)])

class Plan(models.Model):
    _name = 'maint.plan'
    _description = 'Plan de mantenimientos'

    name = fields.Char(string='Nombre')
    program = fields.One2many('maint.program', 'plan_id', string='Mantenimientos')
