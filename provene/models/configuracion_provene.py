# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import models, fields, api

class valorManifiesto(models.Model):

    _name = 'manifiesto.valor'
    _order = 'id desc'
    _rec_name = 'manifiesto_nombre'

    manifiesto_nombre = fields.Char(string = 'Manifiesto', default= 'Manifiesto')
    manifiesto_valor = fields.Html(string = 'Manifiesto')   



class valorInstrucciones(models.Model):

    _name = "instruccion.valor"
    _rec_name = 'instruccion_valor'
    instruccion_valor = fields.Char(string='Tipo de Documento')
    requisito_documento = fields.Html(string='Requisitos:')
    Procedimiento_documento = fields.Html(string='Procedimiento:')

   

class valorAsesoria(models.Model):

    _name = "asesoria.valor"
    _rec_name = 'asesoria_valor'
    asesoria_valor = fields.Char(string='Tipo de Asesoria')


class valorDirectorio(models.Model):

    _name = "directorio.valor"
    _rec_name = 'directorio_valor'
    directorio_valor = fields.Char(string='Nombre de la Institución')
    parroquia = fields.Many2one('res.country.state.municipality.parish', string='Parroquia', domain="[('municipality_id', '=', municipio)]")
    municipio = fields.Many2one('res.country.state.municipality', string='Municipio', domain="[('state_id', '=', estado)]")
    estado = fields.Many2one('res.country.state', string='Estado', domain="[('country_id', '=', nacionalidad)]")
    nacionalidad = fields.Many2one('res.country', string='Nacionalidad', default = 238)
    direccion_institucion = fields.Text(string='Dirección de la Institución')