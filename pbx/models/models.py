# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json
from datetime import timedelta


class Number(models.Model):
    _name = 'pbx.number'
    _order = "number asc"
    _description = 'Numero PBX'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'number'
    _sql_constraints = [
        ('unique_number', 'unique (number)', 'Este numero ya existe')
    ]    
    number = fields.Char(string="Numero", help='Registrar numero', required=True, index=True, tracking=True,)
    num_category = fields.Selection([('extension', 'Extension'), ('virtual', 'Virtual'), ('direct', 'Directo')], required=True, string='Categoria', default="extension")
    num_status = fields.Selection([('free', 'Libre'), ('assigned', 'Asignado')], required=True, string='Estado', default="assigned")
    num_type = fields.Selection([('analog', 'Analogico'), ('digital', 'Digital'), ('ip', 'IP')], required=True, string='Tipo', default="analog", tracking=True,)
    phonebook_ids = fields.Many2many('pbx.phonebook', relation="partner_numbers", string='Asignado a', tracking=True,)
    point_ids = fields.One2many('pbx.point', 'number_id',  string='Puntos en cableado',  ondelete='set null')
    out_permission = fields.Selection([('0', 'Sin salida'), ('1', 'Convencional'), ('2', 'Convencional | Celular'),
                                       ('3', 'Convencional | Celular | Internacional')],
                                      required=False, string='Permisos de salida')
    address = fields.Char(string="Direccion logica", required=False, tracking=True,)
    capture_group = fields.Char(string="Grupo de captura", required=False, tracking=True,)
    comments = fields.Text(string="Observacion",  required=False, tracking=True,)

    def get_area(self):
        if len(self.phonebook_ids) >= 1:
            return self.phonebook_ids[0].area_id.name
        return None

    def get_parent_area(self):
        if len(self.phonebook_ids) >= 1:
            if self.phonebook_ids[0].area_id.area_id:
                return f"{self.phonebook_ids[0].area_id.area_id.name}"
        return None

    def get_puntos(self):
        for p in self.point_ids:
            if "C2-E2-2CT01-A01" in p.full_code:
                return p.full_code
        return None

    def get_abonado(self):
        if len(self.phonebook_ids) > 1:
            return None
        if len(self.phonebook_ids) == 1:
            return self.phonebook_ids[0].partner_id.name
        return None

    def get_position(self):
        if len(self.phonebook_ids) > 1:
            return None
        if len(self.phonebook_ids) == 1:
            return self.phonebook_ids[0].position_id.name
        return None


class Point(models.Model):
    _name = 'pbx.point'
    _order = "full_code asc"
    _description = 'Punto de cableado'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'full_code'
    _sql_constraints = [
        ('unique_full_code', 'unique (full_code)', 'Este codigo ya existe')
    ] 
    
    @api.depends('room_id', 'rack_id', 'space_id', 'point')
    def compute_code(self):
        for rec in self:
            self._create_point_code(rec)

    @staticmethod
    def _create_point_code(rec):
        if rec.room_id:
            rec.full_code = f"{rec.room_id.building_id.campus_id.code}-{rec.room_id.building_id.code}-{rec.room_id.code}"
        if rec.rack_id:
            rec.full_code += f"-{rec.rack_id.code}"
        if rec.space_id:
            rec.full_code += f"-{rec.space_id.code}"
        if rec.point:
            rec.full_code += f"-{rec.point}"
        if not rec.full_code:
            rec.full_code = "Nuevo"

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args  = args or []
        domain = []
        if name:
            domain = ['|', '|', '|', 
                      ('full_code', operator, name), 
                      ('number_id.number', operator, name), 
                      ('room_id.name', operator, name), 
                      ('rack_id.name', operator, name)
                    ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
        
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if not default:
            default = {}
        if not default.get('code'):
            default['point'] = f"{self.point}?"
        return super(Point, self).copy(default)
    
    @api.onchange('room_id')
    def room_on_change(self):
        for rec in self:
            rec.rack_id = None
            rec.space_id = None
            return {'domain': {'rack_id': [('room_id', '=', rec.room_id.id)]}}
    
    @api.onchange('rack_id')
    def rack_on_change(self):
        for rec in self:
            rec.space_id = None    
            return {'domain': {'space_id': [('rack_id', '=', rec.rack_id.id)]}}

    number_id = fields.Many2one('pbx.number', ondelete="set null", string='Numero', tracking=True, copy=False)
    room_id = fields.Many2one('pbx.room', ondelete="cascade", string='Cuarto', required=True, tracking=True,)
    rack_id = fields.Many2one('pbx.room.rack', ondelete="cascade", string='Rack', required=True, tracking=True,)
    space_id = fields.Many2one('pbx.rack.space', ondelete="cascade", string='Espacio', required=True, tracking=True,)
    point = fields.Char(string="Punto/Par", required=True, tracking=True, default="")
    
    full_code = fields.Char(string="Codigo punto", readonly=True, compute="compute_code", store=True)

    origin_id = fields.Many2one('pbx.point', ondelete="set null", string='Origen', required=False, tracking=True, copy=False)
    destination_id = fields.Many2one('pbx.point', ondelete="set null", string='Destino', required=False, tracking=True, copy=False)
    comment = fields.Text(string="Observacion", required=False, tracking=True, copy=False)

    def get_origin(self):
        if self.origin_id:
            origin_full_code = self.origin_id.full_code
            if origin_full_code.startswith(self.room_id.building_id.campus_id.code):
                origin_full_code = origin_full_code.replace(self.room_id.building_id.campus_id.code, "").strip('-')
            if origin_full_code.startswith(self.room_id.building_id.code):
                origin_full_code = origin_full_code.replace(self.room_id.building_id.code, "").strip('-')
            if origin_full_code.startswith(self.room_id.code):
                origin_full_code = origin_full_code.replace(self.room_id.code, "").strip('-')
            if origin_full_code.startswith(self.rack_id.code):
                origin_full_code = origin_full_code.replace(self.rack_id.code, "").strip('-')
            return origin_full_code
        return ""

    def get_rack_position(self):
        return f"{self.rack_id.code}-{self.space_id.code}-{self.point}"

    def update_point_code(self):
        for rec in self:
            self._create_point_code(rec)

    
class Phonebook(models.Model):
    _name = 'pbx.phonebook'
    _description = 'Directorio'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'partner_id'
    
    _sql_constraints = [
        ('unique_partner_id', 'unique (partner_id)', 'La relacion entre la persona y el numero ya existe')
    ]   
    
    @api.onchange('area_id')
    def area_on_change(self):
        for rec in self:
            rec.position_id = None
            return {'domain': {'position_id': [('area_id', '=', rec.area_id.id)]}}
        
    partner_id = fields.Many2one('res.partner', ondelete="cascade", string='Asignado a', tracking=True, copy=False)
    number_ids = fields.Many2many('pbx.number', relation="partner_numbers", string='Numeros asignados')
    area_id = fields.Many2one('pbx.area', string='Area')
    position_id = fields.Many2one('pbx.position', string='Cargo')


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.depends('date_start', 'duration', 'duration_unit')
    def compute_deadline(self):
        for rec in self:
            if rec.duration_unit == 'day' and rec.date_start:
                rec.date_deadline = (rec.date_start + timedelta(days=rec.duration)) - 1
            if rec.duration_unit == 'week' and rec.date_start:
                rec.date_deadline = (rec.date_start + timedelta(weeks=rec.duration)) - 1

    date_start = fields.Date(string='Fecha inicio')
    duration = fields.Integer(string='Duracion de tarea')
    duration_unit = fields.Selection([('day', 'Día'), ('week', 'Semana')], string='Unidad de duracion', default="week")
    date_deadline = fields.Date(string='Fecha límite', readonly=False, compute="compute_deadline", store=True)
