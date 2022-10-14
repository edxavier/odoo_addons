# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: LINTO C T(<https://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api
from datetime import datetime, timedelta

class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.depends('start_date', 'duration', 'duration_unit')
    def _compute_deadline(self):
        for rec in self:
            if rec.duration_unit == 'day' and rec.start_date:
                rec.date_deadline = rec.start_date + timedelta(days=rec.duration)
            if rec.duration_unit == 'week' and rec.start_date:
                rec.date_deadline = rec.start_date + timedelta(weeks=rec.duration)
                
            
                
    start_date = fields.Date(string='Fecha inicio')
    duration = fields.Integer(string='Duracion de tarea')
    duration_unit = fields.Selection([('day', 'Día'), ('week', 'Semana')], string='Unidad de duracion', default="week")
    date_deadline = fields.Date(string='Fecha límite', readonly=True, compute="_compute_deadline", store=True)



