# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Number(models.Model):
    _name = 'pbx.number'
    _description = 'Numero PBX'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'number'
    _sql_constraints = [
        ('unique_number', 'unique (number)', 'Este numero ya existe')
    ]    
    number = fields.Char(string="Numero", help='Registrar numero', required=True, index=True)
    num_category= fields.Selection([('extension', 'Extension'), ('virtual', 'Virtual'), ('direct', 'Directo')], required=True, string='Categoria', default="extension")
    num_status = fields.Selection([('free', 'Libre'), ('assigned', 'Asignado')], required=True, string='Estado', default="assigned")
    num_type = fields.Selection([('analog', 'Analogico'), ('digital', 'Digital'), ('ip', 'IP')], required=True, string='Tipo', default="analog")
    phonebook_ids = fields.Many2many('pbx.phonebook', relation="partner_numbers", string='Asignado a')
    point_ids =  fields.One2many('pbx.point', 'number_id',  string='Puntos en cableado',  ondelete='set null')

   
class Point(models.Model):
    _name = 'pbx.point'
    _description = 'Punto de cableado'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'full_code'
    _sql_constraints = [
        ('unique_full_code', 'unique (full_code)', 'Este codigo ya existe')
    ] 
    
    @api.depends('building_id', 'room_id', 'code', 'space_id')
    def _compute_code(self):
        for rec in self:
            if rec.building_id:
                rec.full_code = f"{rec.building_id.full_code}"
            if rec.room_id:
                rec.full_code = f"{rec.room_id.full_code}"
            if rec.space_id:
                rec.full_code = f"{rec.space_id.full_code}"
            if rec.code:
                rec.full_code += f"-{rec.code}"
            if not rec.full_code:
                rec.full_code = "Nuevo"
                
    @api.onchange('building_id')
    def building_on_change(self):
        for rec in self:
            rec.room_id = None
            return {'domain': {'room_id': [('building_id', '=', rec.building_id.id)]}}
        
    @api.onchange('room_id')
    def room_on_change(self):
        for rec in self:
            rec.space_id = None
            return {'domain': {'space_id': [('room_id', '=', rec.room_id.id)]}}
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args  = args or []
        domain = []
        if name:
            domain = ['|', '|', '|', 
                      ('full_code', operator, name), 
                      ('number_id.number', operator, name), 
                      ('room_id.name', operator, name), 
                      ('code', operator, name)
                    ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
        
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if not default:
            default = {}
        if not default.get('code'):
            default['code'] = f"{self.code}(copy)"
        return super(Point, self).copy(default)
        
    
    full_code = fields.Char(string="Codigo punto", readonly=True, compute="_compute_code", store=True)
    #origin_id = fields.Many2one('pbx.point', ondelete="set null",
    #                                 string='Origen', required=False, tracking=True)
    destination_id = fields.Many2one('pbx.point', ondelete="set null",
                                     string='Destino', required=False, tracking=True)
    number_id = fields.Many2one('pbx.number', ondelete="set null", string='Numero', tracking=True)
    building_id = fields.Many2one('pbx.building', ondelete="cascade", string='Edificio', required=True, tracking=True)
    room_id = fields.Many2one('pbx.room', ondelete="cascade", string='Cuarto', required=True, tracking=True)
    space_id = fields.Many2one('pbx.room.space', ondelete="cascade", string='Ubicaion en el cuarto', 
                               required=True, tracking=True, help='Ej: A01, RK01')
    code = fields.Char(string="Codigo de ubicacion", required=True, tracking=True, 
                       help='Ej: U01-T1-P2 (Unidad de rack 01, Terminal 1, Par 2)')
    comment = fields.Text(string="Observacion", required=False, tracking=True, 
                       help='Ubicacion dentro del rack o dentro del espacio de trabajo')
    
    
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
    
