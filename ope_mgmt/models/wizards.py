from odoo import models, fields, api


class CloseIncident(models.TransientModel):
    _name = 'ope.incident.close'

    source = fields.Selection([('internal', 'Interno'), ('external', 'Externo'), ('unknown', 'Desconocido')], string='Origen del incidente', required=True, default='internal', tracking=True)
    closing_comment = fields.Text(string='Comentario de cierre', help='Especifique en resumen la causa y solucion al incidente', required=True)
    attended_by = fields.Many2many('res.partner', string='Atendido por', required=True)

    def close_incident(self):
        incindent_id = self._context.get('incindent_id')
        Incident = self.env['ope.incident']    
        i = Incident.search([('id', '=', incindent_id)])[0]
        
        for o in self:
            i.source = o.source
            i.closing_comment = o.closing_comment
            i.attended_by = o.attended_by
            i.state = 'closed'