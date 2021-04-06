from odoo import models, fields, api


MONTHS = [('Enero', 'ENERO'), ('Febrero', 'FEBRERO'), 
                ('Marzo', 'MARZO'), ('Abril', 'ABRIL'), 
                ('Mayo', 'MAYO'),('Junio', 'JUNIO'), ('Julio', 'JULIO'),
                ('Agosto', 'AGOSTO'),('Septiembre', 'SEPTIEMBRE'),
                ('Octubre', 'OCTUBRE'),('Noviembre', 'NOVIEMBRE'),('Diciembre', 'DICIEMBRE'),]

class TurnChange(models.Model):
    _name = 'sched.turn.change'
    _description = 'Cambios de turno'

    """@api.model
    def get_emp_domain(self):
        cats = self.env['res.partner.category'].search([('name', '=', 'Ing. Mantto. Radar')])
        ids = []
        for cat in cats:
            ids.append(cat.id)
        return [('is_company', '=', False), ('category_id','in', ids)]"""
    
    name = fields.Char(default='Nuevo cambio de turno',)
    #requested_by = fields.Many2one('res.partner', string='Quien solicita', required=True, domain=lambda self: self.get_emp_domain())
    #accepted_by = fields.Many2one('res.partner', string='Quien acepta', required=True, domain=lambda self: self.get_emp_domain())
    requested_by = fields.Many2one('cmdb.technician', string='Quien solicita', required=True)
    accepted_by = fields.Many2one('cmdb.technician', string='Quien acepta', required=True)
    original_turn = fields.Many2one('sched.turn', string='Turno a cambiar', required=True)
    required_turn = fields.Many2one('sched.turn', string='Turno deseado', required=True)
    original_turn_date = fields.Date(string="Fecha del turno a cambiar", required=True)
    required_turn_date = fields.Date(string="Fecha del turno requerido", required=True)
    sched_month = fields.Selection(MONTHS, string='Mes de roll de trabajo', default='Enero')
    use_signature = fields.Boolean(default=True, string='Usar firma digital')

    
    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo cambio de turno') == 'Nuevo cambio de turno':
            vals['name'] = self.env['ir.sequence'].next_by_code('sched.turn.change.sequence') or 'Nuevo cambio de turno'
        return super(TurnChange, self).create(vals)


class Permission(models.Model):
    _name = 'sched.permission'
    _description = 'Permiso de 1/2 a 3 dias'
    _rec_name = 'requested_by'

    @api.onchange('requested_by')
    def compute_code(self):
        for rec in self:
            rec.code = rec.requested_by.employe_number

    @api.onchange('requested_by2')
    def compute_code2(self):
        for rec in self:
            rec.code2 = rec.requested_by2.employe_number

    requested_by = fields.Many2one('cmdb.technician', string='Solicitante',)
    code = fields.Char(string='Código empleado')
    required_date = fields.Date(string="Fecha del permiso", )
    count_as = fields.Selection([('vacations', 'Vacaciones'), ('salry', 'Salario'), ('earning_salry', 'Con goce de salario')], string='A cuenta de', default='vacations')
    comment = fields.Char(string='Justificación')
    perm_time = fields.Char(string='Tiempo')

    requested_by2 = fields.Many2one('cmdb.technician', string='Solicitante')
    code2 = fields.Char(string='Código empleado')
    required_date2 = fields.Date(string="Fecha del permiso", )
    count_as2 = fields.Selection([('vacations', 'Vacaciones'), ('salry', 'Salario'), ('earning_salry', 'Con goce de salario')], string='A cuenta de', default='vacations')
    comment2 = fields.Char(string='Justificación')
    perm_time2 = fields.Char(string='Tiempo')
