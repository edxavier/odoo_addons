from odoo import models, fields, api


class Incident(models.Model):
    _name = 'ope.incident'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'ope.event': 'event_id'} 
    
    _description = 'Incidente'
    _order = "create_date desc"

    event_id = fields.Many2one('ope.event', ondelete="cascade", required=True, auto_join=True)     

    incident_code = fields.Char(string="Codigo", required=True, copy=False, readonly=True, index=True, default='Nuevo')
    reported_by = fields.Many2one('res.partner', string='Reportado por', tracking=True, required=True,)
    reported_to = fields.Many2one('res.partner', string='Reportado a', required=True,)
    reported_datetime = fields.Datetime(string="Fecha y hora del reporte", required=True)
    reported_media = fields.Selection([('phone', 'Telefono'), ('email', 'Email'), ('person', 'En persona'), ('sms', 'Mensajeria')], 
                                        required=True, default='phone', string='Medio de notificacion', tracking=True)


    source = fields.Selection([('internal', 'Interno'), ('external', 'Externo'), ('unknown', 'Desconocido')], string='Origen del incidente', required=True, default='internal', tracking=True)
    state = fields.Selection([('draft', 'Borrador'), ('open', 'Abierto'), ('tracking', 'En seguimiento'), ('canceled', 'Cancelado'), ('closed', 'Cerrado')], required=True, string='Estado', default='draft', tracking=True)
    
    attended_by = fields.Many2many('res.partner', string='Personas asociadas al incidente', tracking=True)
    related_incident = fields.Many2one('ope.incident', string='Incidente relacionado',)
    finish_datetime = fields.Datetime(string="Fecha y hora finalizacion")

    affected_customers = fields.Many2many('cmdb.customer', string='Unidades cliente afectadas',)
    related_items = fields.Many2many('cmdb.item', string='Items relacionados',)
    affected_services = fields.Many2many('cmdb.service', string='Servicios afectados',)
    #failures = fields.Many2many('cmdb.failures', string='Fallos asociados',)




    @api.model
    def create(self, vals):
        if vals.get('incident_code', 'Nuevo') == 'Nuevo':
            vals['incident_code'] = self.env['ir.sequence'].next_by_code('ope.incident.sequence') or 'Nuevo'
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