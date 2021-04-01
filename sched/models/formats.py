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

