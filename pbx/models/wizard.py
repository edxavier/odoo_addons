from odoo import models, fields, api


class PbxPointReportWizard(models.TransientModel):
    _name = 'pbx.point.report'
    _description = 'Reporte de puntos telefonia'

    title = fields.Char(string="Encabezado")
    type = fields.Selection([('point', 'Punto'), ('number', 'Numero')], string='Tipo de reporte', default="point")
    room_id = fields.Many2one('pbx.room', string='Cuarto')
    rack_id = fields.Many2one('pbx.room.rack', string='Rack')

    def print_report(self):
        room_domain = None
        rack_domain = None
        if self.room_id.id is not False:
            room_domain = ('room_id', '=', self.room_id.id)
        if self.rack_id.id is not False:
            rack_domain = ('rack_id', '=', self.rack_id.id)
        my_data = {
            'room_domain': room_domain,
            'rack_domain': rack_domain,
            'title': self.title
        }
        #return self.env.ref('pbx.rack_points_action_report').with_context(landscape=True).report_action(self, data)
        print(self.type)
        if self.type == 'point':
            return self.env.ref('pbx.rack_points_action_report').report_action(self, data=my_data)
        else:
            return self.env.ref('pbx.rack_points_action_report').report_action(self, data=my_data)


class PbxPointReport(models.AbstractModel):
    _name = 'report.pbx.report_points'
    _description = 'Reporte de puntos telefonia2'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        room_domain = data.get('room_domain')
        rack_domain = data.get('rack_domain')
        _domain = []
        if room_domain:
            _domain.append(room_domain)
        if rack_domain:
            _domain.append(rack_domain)
        grouped_rooms = self.env['pbx.point'].read_group(
            domain=_domain,
            fields=['room_id'],
            groupby=['room_id'],
            orderby='room_id asc'
        )
        points = []
        for room in grouped_rooms:
            _room = self.env['pbx.room'].browse(room.get('room_id')[0])
            print(_room.name)
            _domain = [('room_id', '=', _room.id),]
            if rack_domain:
                _domain.append(rack_domain)
            grouped_racks = self.env['pbx.point'].read_group(
                domain=_domain,
                fields=['rack_id'],
                groupby=['rack_id'],
                orderby='rack_id asc'
            )
            room_racks = []
            for rack in grouped_racks:
                _rack = self.env['pbx.room.rack'].browse(rack.get('rack_id')[0])
                print(_rack.name)
                print("--------------------------------")
                _domain = [('room_id', '=', _room.id), ('rack_id', '=', _rack.id)]
                grouped_spaces = self.env['pbx.point'].read_group(
                    domain=_domain,
                    fields=['space_id'],
                    groupby=['space_id']
                )

                rack_spaces = []
                for space in grouped_spaces:
                    _space = self.env['pbx.rack.space'].browse(space.get('space_id')[0])
                    _domain = [('room_id', '=', _room.id), ('rack_id', '=', _rack.id), ('space_id', '=', _space.id)]
                    points_objs = self.env['pbx.point'].search(_domain, order="full_code asc")
                    rack_spaces.append({
                        'name': f"{_space.name}",
                        'code': f"{_space.code}",
                        'full_code': f"[{_space.full_code}]",
                        'space': f"[{_space.code}] {_space.name}",
                        'points': points_objs
                    })
                room_racks.append({
                  'name': f"{_rack.name}",
                  'code': f"{_rack.code}",
                  'rack': f"[{_rack.code}] {_rack.name}",
                  'spaces': rack_spaces
                })
                    
            points.append({
                'name': f"{_room.name}",
                'room': f"[{_room.full_code}] {_room.name}",
                'racks': room_racks
            })

        docargs = {
            'doc_ids': docids,
            'doc_model': 'pbx.point',
            'docs': points,
            'title': data.get('title', ''),
            'report_type': data.get('report_type'),
        }
        return docargs
