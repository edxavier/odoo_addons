# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Municipality(models.Model):
    _name = 'provet.municipality'
    _description = 'Municipio'

    name = fields.Char(required=True)
    state_id = fields.Many2one('res.country.state', string='Departamento', required=True)


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('state_id')
    def state_on_change(self):
        for rec in self:
            rec.municipality_id = None
            return {'domain': {'municipality_id': [('state_id', '=', rec.state_id.id)]}}

    @api.onchange('municipality_id')
    def municipality_on_change(self):
        for rec in self:
            rec.state_id = rec.municipality_id.state_id
            rec.city = rec.municipality_id.name

    def default_country(self):
        return self.env['res.country'].search([('code', '=', 'NI')], limit=1).id

    municipality_id = fields.Many2one('provet.municipality', string='Municipio')
    country_id = fields.Many2one('res.country', string='País', default=default_country)
    doc_id = fields.Char(string="Numero de identificacion")




