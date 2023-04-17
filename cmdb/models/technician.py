# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning

class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    def become_technician(self):
        for o in self:
            if self.is_technician():
                raise Warning("Ya existe un perfil técnico para este contacto")
            else:
                self.env['cmdb.technician'].create({'partner_id': o.id})
                return {
                    'effect': {
                        'fadeout': 'slow',
                        'title': 'Aviso!',
                        'message': 'Perfil técnico creado',
                        'type': 'rainbow_man',
                    }
                }


    def generate_user(self):
        for o in self:
            if not self.has_user():
                User = self.env['res.users']
                splited_name = o.name.split(' ')
                if splited_name.__len__() > 1:
                    login_name = f"{splited_name[0][0].lower()}{splited_name[1].lower()}"
                else:
                    login_name = splited_name[0].lower()

                user_access = {
                    'login': login_name,
                    'password': '123456',
                    'partner_id': o.id
                }
                User.create(user_access)
                return {
                        'effect': {
                            'fadeout': 'slow',
                            'title': 'Aviso!',
                            'message': 'Usuario creado',
                            'type': 'rainbow_man',
                        }
                }
            else:
                raise Warning(f"Ya existe un usuario para este contacto")
        



    @api.model
    def is_technician(self):
        for o in self:
            if o.company_type == 'person':
                Technician = self.env['cmdb.technician']
                # Buscar si ya existe un perfil para este contacto
                profiles_count = Technician.search_count([('partner_id', '=',  o.id)])
                o.has_tech_profile = profiles_count > 0
                return profiles_count > 0
            else:
                o.has_tech_profile = True
                return True

    def has_user(self):
        for o in self:
            Technician = self.env['res.users']
            # Buscar si ya existe un perfil para este contacto
            profiles_count = Technician.search_count([('partner_id', '=',  o.id)])
            return profiles_count > 0
            

    employe_number = fields.Char("Numero de empleado", default="0")
    has_tech_profile = fields.Boolean(compute="is_technician", store=False)
    #technician_id = fields.Many2one('cmdb.technician', string="Enlace al perfil tecnico") 

    
   

class Technician(models.Model):
    _name = 'cmdb.technician'
    _description = 'Personal técnico'
    _inherits = {'res.partner': 'partner_id'} 
    
    partner_id = fields.Many2one('res.partner', ondelete="cascade", required=True, auto_join=True) 
    
    #take_turns = fields.Boolean(default=True, string="Realiza turnos")
    #freeze_turn = fields.Boolean(default=False, string="Mantener el mismo turno", help="Se mantentra siempre el ultimo turno realizado")
    signature = fields.Image(string="Firma digital")
    active = fields.Boolean(default=True, string="Activo")