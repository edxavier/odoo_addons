from odoo import models, fields, api

class EventTracking(models.Model):
    _name = 'ope.event.tracking'
    _description = 'Seguimiento de evento'
    _rec_name = 'event_id'

    event_id = fields.Many2one('ope.event', string='Evento', ondelete='cascade',)
    event_date = fields.Datetime(string="Fecha", required=True)
    note = fields.Text(string='Nota', required=True)
    attach = fields.Binary(string="Adjuntar archivo")


class Event(models.Model):
    _name = 'ope.event'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Evento'
    _order = "create_date desc"

    event_code = fields.Char(string="Codigo", required=True, copy=False, readonly=True, index=True, default='Nuevo')
    name = fields.Char(string="Titulo", required=True, tracking=True)
    description = fields.Text(string='Descripcion', required=True, tracking=True)
    tracking = fields.One2many('ope.event.tracking', 'event_id', string=' Nota de Seguimiento', ondelete='cascade', tracking=True)


    @api.model
    def create(self, vals):
        if vals.get('event_code', 'Nuevo') == 'Nuevo':
            vals['event_code'] = self.env['ir.sequence'].next_by_code('ope.event.sequence') or 'Nuevo'
        #vals['state'] = 'open'
        return super(Event, self).create(vals)