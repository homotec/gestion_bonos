# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError


import uuid
from datetime import date

class Coupon(models.Model):
    _name = 'gestion_bonos.coupon'
    _description = 'Coupon'

    name = fields.Char(string='Nombre', required=True)
    creation_date = fields.Date(string='Fecha Creacion', default=fields.Date.today())
    expiration_date = fields.Date(string='Fecha Cancelacion')
    discount_type = fields.Selection([
        ('porcentaje', 'Porcentaje'),
        ('cantidad', 'Cantidad'),
    ], string='Tipo de Descuento', default='cantidad')    
    discount = fields.Float(string='Descuento', required=True)
    customer_id = fields.Many2one('res.partner', string='Cliente', required=True)
    units = fields.Integer(string='Unidades', help='Aquí puedes ingresar la cantidad de unidades de producto a las que se aplica el descuento.')
    product_id = fields.Many2one('product.product', string='Producto')
    token = fields.Char(string='Token', required=True, readonly=True, copy=False, default=lambda self: str(uuid.uuid4()))
    estado = fields.Selection([
        ('activo', 'Activo'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', default='activo')

    @api.onchange('estado')
    def _onchange_estado(self):
        for record in self:
            if record.estado == 'cancelado':
                record.expiration_date = date.today()
            elif record.estado == 'activo':
                record.expiration_date = False
    
    @api.constrains('discount', 'discount_type')
    def _check_discount(self):            
        for record in self:
            if record.discount_type and record.discount:
                if record.discount_type == 'porcentaje' and record.discount < 0:
                    raise exceptions.ValidationError('El descuento no puede ser negativo cuando el tipo de descuento es porcentaje.')
                if record.discount_type == 'cantidad' and record.discount < 0:
                    raise exceptions.ValidationError('El descuento no puede ser negativo cuando el tipo de descuento es cantidad.')
                if record.discount_type == 'porcentaje' and not (1 <= record.discount <= 100):
                    raise exceptions.ValidationError('El descuento debe estar entre 1 y 100 cuando el tipo de descuento es porcentaje.')
                

class DuplicateWizard(models.TransientModel):
    _name = 'gestion_bonos.duplicate_wizard'
    _description = 'Wizard para duplicar registros'

    num_copies = fields.Integer(string='Número de Copias', required=True)

    def duplicate_record(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            record = self.env['gestion_bonos.coupon'].browse(active_id)
            for _ in range(self.num_copies):
                record.copy()
