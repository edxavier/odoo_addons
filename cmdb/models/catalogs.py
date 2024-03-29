# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Building(models.Model):
    _name = 'cmdb.building'
    _description = 'Edificio'

    name = fields.Char(string="Nombre", required=True, )
    active = fields.Boolean(default=True)

class Office(models.Model):
    _name = 'cmdb.office'
    _description = 'Oficina'

    name = fields.Char(string="Nombre", required=True)
    building = fields.Many2one('cmdb.building', ondelete="cascade",  required=True, string='Edificio')
    active = fields.Boolean(default=True)


class System(models.Model):
    _name = 'cmdb.system'
    _description = 'Sistema'

    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean(default=True)

class Subsystem(models.Model):
    _name = 'cmdb.subsystem'
    _description = 'Subsistema'

    name = fields.Char(string="Nombre", required=True)
    system = fields.Many2one('cmdb.system', required=True, ondelete="cascade", string='Sistema')
    active = fields.Boolean(default=True)

class Manufacturer(models.Model):
    _name = 'cmdb.manufacturer'
    _description = 'Marca'

    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean(default=True)

class ManufacturerModel(models.Model):
    _name = 'cmdb.model'
    _description = 'Modelo'

    name = fields.Char(string="Nombre", required=True)
    manufacturer = fields.Many2one('cmdb.manufacturer', required=True, ondelete="cascade", string='Marca')
    active = fields.Boolean(default=True)



class ServiceStatus(models.Model):
    _name = 'cmdb.service.status'
    _description = 'Estado de servicio'

    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean(default=True)


class ServiceType(models.Model):
    _name = 'cmdb.service.type'
    _description = 'Tipo de servicio'

    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean(default=True)


class AssetType(models.Model):
    _name = 'cmdb.asset.type'
    _description = 'Tipo de activo'

    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean(default=True)

class Failure(models.Model):
    _name = 'cmdb.failure'
    _description = 'Fallo'

    name = fields.Char(string="Nombre", required=True)
    type = fields.Selection([('other', 'Otro'), ('hard', 'Componente hardware'), ('soft', 'Software'), ('person', 'Humano'),
     ('net', 'Red'), ('phone', 'Telefonia'), ('radio', 'Radio'), ('structure', 'Infraestructura'), ('external', 'Externo')], required=True, string='Tipo de fallo')
    active = fields.Boolean(default=True)