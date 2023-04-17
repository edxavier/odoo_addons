# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Campus(models.Model):
    _name = 'pbx.campus'
    _description = 'Campo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Campo", required=True, index=True, tracking=True)
    code = fields.Char(string="Codigo", help='Codigo', tracking=True)


class Building(models.Model):
    _name = 'pbx.building'
    _description = 'Edificio'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [
        ('unique_full_code', 'unique (full_code)', 'Este codigo ya existe')
    ] 
    
    @api.depends('campus_id', 'code')
    def compute_code(self):
        for rec in self:
            self.generate_code(rec)

    @staticmethod
    def generate_code(rec):
        if rec.campus_id and rec.code:
            rec.full_code = f"{rec.campus_id.code}-{rec.code}"
        elif rec.campus_id:
            rec.full_code = f"{rec.campus_id.code}"
        elif rec.code:
            rec.full_code = f"{rec.code}"
        else:
            rec.full_code = "Nuevo"

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args  = args or []
        domain = []
        if name:
            domain = ['|', '|', '|',
                      ('name', operator, name), 
                      ('campus_id.name', operator, name), 
                      ('code', operator, name),
                      ('full_code', operator, name)
                    ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
                
    campus_id = fields.Many2one('pbx.campus', ondelete="cascade", string='Campus', required=True, tracking=True)
    name = fields.Char(string="Edificio", required=True, tracking=True)
    code = fields.Char(string="Codigo", required=True, index=True, tracking=True, copy=False)
    full_code = fields.Char(string="ID", readonly=True, compute="compute_code", store=True)
    
    def name_get(self):
        results = []
        for rec in self:
            if self.env.context.get('hide_code'):
                name = f"{rec.name}"
            else:
                name = f"[{rec.full_code}] {rec.name}"
            results.append((rec.id, name))
        return results


class Room(models.Model):
    _name = 'pbx.room'
    _description = 'Cuarto'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [
        ('unique_full_code', 'unique (full_code)', 'Este codigo ya existe')
    ] 
    
    @api.depends('building_id', 'code')
    def compute_code(self):
        for rec in self:
            if rec.building_id and rec.code:
                rec.full_code = f"{rec.building_id.full_code}-{rec.code}"
            elif rec.building_id:
                rec.full_code = f"{rec.building_id.full_code}"
            elif rec.code:
                rec.full_code = f"{rec.code}"
            else:
                rec.full_code = "Nuevo"
    
    def name_get(self):
        results = []
        for rec in self:
            if self.env.context.get('hide_code', True):
                name = f"{rec.name}"
            else:
                name = f"[{rec.full_code}] {rec.name}"
            results.append((rec.id, name))
        return results

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args  = args or []
        domain = []
        if name:
            domain = ['|', '|', '|', 
                      ('name', operator, name), 
                      ('building_id.name', operator, name), 
                      ('code', operator, name),
                      ('full_code', operator, name)
                    ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
             
    name = fields.Char(string="Nombre cuarto", required=True, tracking=True)
    building_id = fields.Many2one('pbx.building', ondelete="cascade", string='Edificio', required=True, tracking=True)
    code = fields.Char(string="Codigo", required=True, index=True, tracking=True, copy=False)
    full_code = fields.Char(string="ID", readonly=True, compute="compute_code", store=True)


class Rack(models.Model):
    _name = 'pbx.room.rack'
    _order = "full_code asc"
    _description = 'Rack/Gabinete'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [
        ('unique_full_code', 'unique (full_code)', 'Este codigo ya existe')
    ] 
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args  = args or []
        domain = []
        if name:
            domain = ['|', '|', '|', 
                      ('name', operator, name), 
                      ('room_id.name', operator, name), 
                      ('code', operator, name),
                      ('full_code', operator, name)
                    ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
    
    @api.depends('room_id', 'code')
    def compute_code(self):
        for rec in self:
            for space in self.space_ids:
                space.compute_code()
            if rec.room_id:
                rec.full_code = f"{rec.room_id.full_code}"
            if rec.code:
                rec.full_code += f"-{rec.code}"
            if not rec.full_code:
                rec.full_code = "Nuevo"
   
    def name_get(self):
        results = []
        for rec in self:
            name = f"[{rec.full_code}] {rec.name}"
            results.append((rec.id, name))
        return results
             
    name = fields.Char(string="Nombre", required=True, tracking=True)
    room_id = fields.Many2one('pbx.room', ondelete="cascade", string='Cuarto', required=True, tracking=True)
    code = fields.Char(string="Codigo", required=True, index=True, tracking=True, help='Ej: A01, RK01', copy=False)
    full_code = fields.Char(string="ID", readonly=True, compute="compute_code", store=True)
    space_ids = fields.One2many('pbx.rack.space', 'rack_id',  string='Espacios/Item',  ondelete='set null')
    
    
class RackSpace(models.Model):
    _name = 'pbx.rack.space'
    _order = "sequence asc"
    _description = 'Espacio/Item en rack'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [
        ('unique_full_code', 'unique (full_code)', 'Este codigo ya existe')
    ] 
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args  = args or []
        domain = []
        if name:
            domain = ['|', '|', '|',
                      ('name', operator, name), 
                      ('rack_id.name', operator, name), 
                      ('code', operator, name),
                      ('full_code', operator, name)
                    ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
    
    @api.depends('rack_id', 'code')
    def compute_code(self):
        for rec in self:
            if rec.rack_id:
                rec.full_code = f"{rec.rack_id.full_code}"
            if rec.code:
                rec.full_code += f"-{rec.code}"
            if not rec.full_code:
                rec.full_code = "Nuevo"
   
    def name_get(self):
        results = []
        for rec in self:
            name = f"[{rec.full_code}] {rec.name}"
            results.append((rec.id, name))
        return results
             
    sequence = fields.Integer(default=1)
    name = fields.Char(string="Nombre", required=True, tracking=True)
    rack_id = fields.Many2one('pbx.room.rack', ondelete="cascade", string='Rack', required=True, tracking=True)
    code = fields.Char(string="Codigo", required=True, index=True, tracking=True, help='Ej: T01, PP01, SW01, SRV01', copy=False)
    full_code = fields.Char(string="Id espacio", readonly=True, compute="compute_code", store=True)
    

class Area(models.Model):
    _name = 'pbx.area'
    _description = 'Area'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [
        ('unique_name', 'unique (name)', 'Este nombre ya existe')
    ]

    def name_get(self):
        results = []
        for rec in self:
            if rec.area_id:
                name = f"{rec.area_id.name} / {rec.name}"
            else:
                name = f"{rec.name}"
            results.append((rec.id, name))
        return results    
    area_id = fields.Many2one('pbx.area', ondelete="set null",
                                     string='Area padre', required=False, tracking=True)
    name = fields.Char(string="Nombre", required=True, tracking=True)


class Position(models.Model):
    _name = 'pbx.position'
    _description = 'Cargo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [
        ('unique_name', 'unique (name, area_id)', 'Este nombre ya existe')
    ]    
    name = fields.Char(string="Nombre", required=True, tracking=True)
    area_id = fields.Many2one('pbx.area', ondelete="cascade", string='Institucion|Area', required=True, tracking=True)

