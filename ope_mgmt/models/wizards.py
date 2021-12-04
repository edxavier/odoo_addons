from odoo import models, fields, api


class CloseIncident(models.TransientModel):
    _name = 'ope.incident.close'

    source = fields.Selection([('internal', 'Interno'), ('external', 'Externo'), ('unknown', 'Desconocido')], string='Origen del incidente', required=True, default='internal', tracking=True)
    closing_comment = fields.Text(string='Comentario de cierre', required=True)
    attended_by = fields.Many2many('res.partner', string='Atendido por', required=True)
    event_date = fields.Datetime(string="Fecha", required=True)


    def close_incident(self):
        incindent_id = self._context.get('incindent_id')
        
        Incident = self.env['ope.incident']    
        Tracking = self.env['ope.event.tracking']    
        i = Incident.search([('id', '=', incindent_id)])[0]
        
        for o in self:
            i.source = o.source
            #i.closing_comment = o.closing_comment
            Tracking.create({
                'event_id': i.event_id,
                'event_date':o.event_date,
                'note': o.closing_comment
            })
            i.attended_by = o.attended_by
            i.state = 'closed'