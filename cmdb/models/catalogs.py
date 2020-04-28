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


class ItemStatus(models.Model):
    _name = 'cmdb.item.status'
    _description = 'Estado de Item'

    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean(default=True)


class ServiceStatus(models.Model):
    _name = 'cmdb.service.status'
    _description = 'Estado de servicio'

    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean(default=True)

class ItemType(models.Model):
    _name = 'cmdb.item.type'
    _description = 'Tipo de Item'

    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean(default=True)

class ServiceType(models.Model):
    _name = 'cmdb.service.type'
    _description = 'Tipo de servicio'

    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean(default=True)

class ComponentType(models.Model):
    _name = 'cmdb.component.type'
    _description = 'Tipo de componente'

    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean(default=True)
