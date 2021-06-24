from odoo import models, fields, api


class IncidentTracking(models.Model):
    _name = 'ope.incident.tracking'
    _description = 'Seguimiento de incidente'
    _rec_name = 'incident_id'

    incident_id = fields.Many2one('ope.incident', string='Incidente', ondelete='cascade',)
    description = fields.Text(string='Descripcion del seguimiento', required=True)
    track_date = fields.Datetime(string="Fecha", required=True)
    attach = fields.Binary(string="Adjutno")
    


class Incident(models.Model):
    _name = 'ope.incident'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Incidente'
    _order = "create_date desc"

    name = fields.Char(string="Codigo incidente", required=True, copy=False, readonly=True, index=True, default='Nuevo')
    reported_by = fields.Many2one('res.partner', string='Reportado por', tracking=True)
    reported_to = fields.Many2one('res.partner', string='Reportado a',)
    reported_media = fields.Selection([('phone', 'Telefono'), ('email', 'Email'), ('person', 'En persona'), ('sms', 'Mensajeria')], required=True, default='phone', string='Medio de notificacion', tracking=True)

    description = fields.Text(string='Incidente', required=True, tracking=True)
    closing_comment = fields.Text(string='Comentario de cierre', help='Especifique en resumen la causa y solucion al incidente')

    source = fields.Selection([('internal', 'Interno'), ('external', 'Externo'), ('unknown', 'Desconocido')], string='Origen del incidente', required=True, default='internal', tracking=True)
    _inherit = ['mail.thread', 'mail.activity.mixin']
    state = fields.Selection([('draft', 'Borrador'), ('open', 'Abierta'), ('tracking', 'En seguimiento'), ('canceled', 'Cancelada'), ('closed', 'Cerrada')], required=True, string='Estado', default='draft', tracking=True)
    
    attended_by = fields.Many2many('res.partner', string='Personas que atendieron el incidente', tracking=True)

    tracking = fields.One2many('ope.incident.tracking', 'incident_id', string='Seguimiento', ondelete='cascade', tracking=True)

    related_incident = fields.Many2one('ope.incident', string='Incidente relacionado',)


    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('ope.incident.sequence') or 'Nuevo'
        vals['state'] = 'open'
        return super(Incident, self).create(vals)
    
    def do_track(self):
        for o in self:
            o.state = 'tracking'
    
    def do_cancel(self):
         for o in self:
            o.state = 'canceled'
    
    def do_close(self):
         for o in self:
            return {    
                'name': "Cierre de incidente",
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'ope.incident.close',
                #'view_id': 'close_incident_wizard',
                'target': 'new',
                'context': {'default_source': o.source, 'default_attended_by': o.attended_by.ids, 'incindent_id': o.id}
            }