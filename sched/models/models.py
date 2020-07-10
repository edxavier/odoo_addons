# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, timedelta
from pprint import pprint
import holidays


class Turn(models.Model):
    _name = 'sched.turn'
    _description = 'Turno'

    name = fields.Char(required=True)
    hours = fields.Integer(default=8)

class Template(models.Model):
    _name = 'sched.template'
    _description = 'Matriz Plantilla'

    name = fields.Char(required=True)
    cicles = fields.One2many('sched.cicle', 'template', string='Ciclos')
    employes = fields.One2many('sched.employe', 'template', string='Empleados')




class Cicle(models.Model):
    _name = 'sched.cicle'
    _description = 'Ciclo'
    #_rec_name = 'sequence'

    @api.depends('day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7')
    def compute_hours(self):
        for rec in self:
            rec.hours = rec.day1.hours + rec.day2.hours + rec.day3.hours + rec.day4.hours + rec.day5.hours + rec.day6.hours + rec.day7.hours 

    @api.depends('hours', 'turn_hours')
    def compute_extras(self):
        for rec in self:
            try:
                extras = rec.hours - rec.turn_hours 
                if extras > 0:
                    rec.extra_hours = extras
                else:
                    rec.extra_hours = 0
            except Exception as e:
                print("#########################################")
                print(e)
                pass

    sequence = fields.Char()
    name = fields.Char(required=True)
    template = fields.Many2one('sched.template', string='Plantilla', required=True)
    day1 = fields.Many2one('sched.turn', string='Lunes')
    day2 = fields.Many2one('sched.turn', string='Martes')
    day3 = fields.Many2one('sched.turn', string='Miercoles')
    day4 = fields.Many2one('sched.turn', string='Jueves')
    day5 = fields.Many2one('sched.turn', string='Viernes')
    day6 = fields.Many2one('sched.turn', string='Sabado')
    day7 = fields.Many2one('sched.turn', string='Domingo')
    hours = fields.Integer(default=0,  compute='compute_hours', store=True)
    turn_hours = fields.Integer(default=48)
    extra_hours = fields.Integer(default=0, compute='compute_extras', store=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'Nuevo') == 'Nuevo':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('sched.cicle.sequence') or 'Nuevo'
        return super(Cicle, self).create(vals)


class EmployeTemp(models.Model):
    _name = 'sched.employe'
    _description = 'Empleado'

    @api.model
    def get_emp_domain(self):
        cats = self.env['res.partner.category'].search([('name', '=', 'Ing. Mantto. Radar')])
        ids = []
        for cat in cats:
            ids.append(cat.id)
        return [('is_company', '=', False), ('category_id','in', ids)]     
    
 
    name = fields.Char(default='--')
    employe = fields.Many2one('res.partner', string='Empleado', required=True, domain=lambda self: self.get_emp_domain())
    last_cicle = fields.Many2one('sched.cicle', string='Ultimo ciclo', domain="[('template', '=', template)]")
    template = fields.Many2one('sched.template', string='Plantilla', required=True)
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('sched.employe.sequence') or 'Nuevo'
        return super(EmployeTemp, self).create(vals)


class Rol(models.Model):
    _name = 'sched.rol'
    _description = 'Rol'

    name = fields.Char(required=True)
    template_id = fields.Many2one('sched.template', string='Plantilla', required=True)
    start_date = fields.Date(string="Inicio de Rol", required=True,)
    weeks = fields.Integer(required=True, string='Semanas', default=4)
    area_boss = fields.Char(string='Jefe Inmediato', default='Ing. Blanca Jarquin')
    deparment_boss = fields.Char(string='Jefe de Departamento', default='Ing. Bismark Incer')
    maint_manager = fields.Char(string='Gerente de mantto.', default='Ing. Noel Gonzales')
    comments = fields.Text(string='Observaciones')
    state = fields.Selection([('draft', 'Borrador'), ('created', 'Creado'), ('generated', 'Generado')], required=True, string='Estado', default='draft')
    schedule_ids = fields.One2many('sched.schedule', 'rol_id', string='Horario')

    @api.model
    def create(self, vals):
        vals['state'] = 'created'
        return super(Rol, self).create(vals)

    def action_generar_horario(self):
        for o in self:
            #o.state = 'generated'
            print("********************************************+")
            weeks_to_generate = o.weeks
            week_to_project = 12
            matrix = [c for c in o.template_id.cicles]
            #print(matrix)
            for e in o.template_id.employes:
                start_date = o.start_date # FECHA DE INICO DEL HORARIO
                #print(e.employe.name)
                #print(e.last_cicle.name)
                #print(e.last_cicle)
                last_cicle = e.last_cicle
                for week in range(0, week_to_project):
                    last_cicle = self.get_next_cicle(matrix, last_cicle)
                    #print("Next cicle")
                    #print(last_cicle)
                    self.generate_turn(o.id, e.employe.id, last_cicle.day1.id, start_date, last_cicle.id)
                    start_date = start_date + timedelta(days=1)

                    self.generate_turn(o.id, e.employe.id, last_cicle.day2.id, start_date, last_cicle.id)
                    start_date = start_date + timedelta(days=1)
                    
                    self.generate_turn(o.id, e.employe.id, last_cicle.day3.id, start_date, last_cicle.id)
                    start_date = start_date + timedelta(days=1)
                    
                    self.generate_turn(o.id, e.employe.id, last_cicle.day4.id, start_date, last_cicle.id)
                    start_date = start_date + timedelta(days=1)
                    
                    self.generate_turn(o.id, e.employe.id, last_cicle.day5.id, start_date, last_cicle.id)
                    start_date = start_date + timedelta(days=1)
                    
                    self.generate_turn(o.id, e.employe.id, last_cicle.day6.id, start_date, last_cicle.id)
                    start_date = start_date + timedelta(days=1)
                    
                    self.generate_turn(o.id, e.employe.id, last_cicle.day7.id, start_date, last_cicle.id)
                    start_date = start_date + timedelta(days=1)

                    
            pass
    def get_next_cicle(self, matrix, last_cicle):
        cicle_index = matrix.index(last_cicle)
        if cicle_index < matrix.__len__()-1:
            cicle_index = cicle_index + 1
        else:
            cicle_index = 0
        return matrix[cicle_index]

    def generate_turn(self, rol_id, emp_id, turn_id, turn_date, cicle_id):
        obj_res = self.env['sched.schedule'].create({
            'rol_id': rol_id,
            'employe_id': emp_id,
            'turn_id': turn_id,
            'cicle_id': cicle_id,
            'turn_date': turn_date,
        })

    def open_horario(self):
        """return {
            'name':'Historial memoria',
            'view_mode':'tree,graph,form',
            'res_model':'net.memory',
            'type':'ir.actions.act_window',
            'domain':[('host_id','=', self.id)],
        }"""
        return {
            'name':'Horario',
            'view_mode':'tree,form,calendar',
            'res_model':'sched.schedule',
            'type':'ir.actions.act_window',
            'domain':[('rol_id','=', self.id)],
        }

    @api.model
    def is_holiday(self, hdate):
        nic_holidays = holidays.CountryHoliday(country='NI', years=2020)
        print(hdate)
        print(nic_holidays)
        print("IS HOLIDAY?")
        print(hdate in nic_holidays)
        return hdate in nic_holidays
        #return "CONTENIDO DE UNA FUNCION"

    def generate_sched_formating(self):
        for o in self:
            print(o.weeks)
            #for e in o.template_id.employes:
            #    print(e.employe.name)
            #print("-------------------------------------------------")
            all_scheds = [s for s in o.schedule_ids]
            num_employes = len(o.template_id.employes)
            num_chunks = int(len(all_scheds)/num_employes)
                            
            #for s in o.schedule_ids:
            
            #print("-------------------------------------------------")
            chunked_scheds = list(self.chunk_list(all_scheds, num_chunks))
            #print(chunked_scheds)

            for i in range(chunked_scheds.__len__()):
                chunked_scheds[i] = list(self.chunk_list(chunked_scheds[i], 7))
            #print("-------------------------------------------------")
            #print(chunked_scheds)
            
            #print("------------------------ROL-------------------------")
            month_rol = []
            #print(o.name)
            #print(all_scheds.__len__())
            #print(chunked_scheds.__len__())
            if all_scheds.__len__() > 0 :
                for w in range(o.weeks):
                    print("+++++++++++++++++++++++++++++ SEMANA: " + str(w+1))
                    week_rol = []
                    for e in chunked_scheds:
                        emp_rol = []
                        for d in range(7):
                            emp_rol.append(e[w][d])
                        week_rol.append(emp_rol)
                    month_rol.append(week_rol)
                    #pprint(week_rol)
                #pprint(month_rol) 

            return month_rol

    def chunk_list(self, mlist, nparts):
        for i in range(0, len(mlist), nparts):
            yield mlist[i:i+nparts]

    def format_date(self, tdate):
           return  tdate.strftime("%a  %d")

    def format_week_date(self, tdate):
           return  tdate.strftime(" %d %B %Y")


class Schedule(models.Model):
    _name = 'sched.schedule'
    _description = 'Horario'
    _rec_name = 'tname'

    @api.depends('turn_date',)
    def compute_date_format(self):
        for rec in self:
           rec.turn_date_str = rec.turn_date.strftime("%a  %d %B %Y")

    @api.depends('employe_id', 'turn_id')
    def compute_name(self):
        for rec in self:
           rec.tname = rec.employe_id.name + "-" + rec.turn_id.name

    tname = fields.Char(string="Turno",  compute='compute_name', store=False,)
    rol_id = fields.Many2one('sched.rol', string='Rol', required=True)
    employe_id = fields.Many2one('res.partner', string='Empleado', required=True)
    turn_id = fields.Many2one('sched.turn', string='Turno', required=True)

    cicle_id = fields.Many2one('sched.cicle', string='Ciclo',)
    turn_date = fields.Date(string="Fecha", )
    turn_date_str = fields.Char(string="Fecha turno",  compute='compute_date_format', store=False,)

  
class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    employe_number = fields.Char("Numero de empleado", default="0")

"""
class ScheduleReport(models.AbstractModel):
    _name = 'report.sched.report_horario2'

    @api.model
    def _get_report_values(self, docids, data=None):
        #employees = self.env['hr.employee'].search([], order='name asc')
        #docs.append({
        #        'employee': employee.name,
        #})
        #return {
        #    'doc_ids': data['ids'],
        #    'doc_model': data['model'],
        #    'docs': docs,
        #}
        print("REPORTE--------------------")
        print(self)
        print(data)
        cats = self.env['res.partner.category'].search([('name', '=', 'Ing. Mantto. Radar')])
        ids = []
        for cat in cats:
            ids.append({
                'name': cat.name,
            })

        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('module.report_horario')

        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': ids,
        }
        print(docargs)
        return docargs
"""