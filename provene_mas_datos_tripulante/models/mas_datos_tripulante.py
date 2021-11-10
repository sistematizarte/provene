# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import models, fields, api
# from bs4 import BeautifulSoup
# from odoo.exceptions import ValidationError
# import requests
# import psycopg2

class MasDatosTripulante(models.Model): 
    _inherit = 'res.users'

    @api.model
    def default_get(self,fields_list):
        res = super(MasDatosTripulante,self).default_get(fields_list)
        
        contenido_manifiesto = self.env['manifiesto.valor'].search([],order='write_date desc',limit=1)
        res.update({'manifiesto':contenido_manifiesto.manifiesto_valor
                    })
        return res       
     
    telefono = fields.Char(
        string='Teléfono',
        required=True
    )        
    
    tipo_tripulante = fields.Selection(
        string='Tipo Tripulante',
        selection=[('pa', 'Embajador'), 
                   ('do', 'Aliado'),
                   ('trac', 'Especialista'),
                   ('trpa','Generoso'),
                   ('vo','Vocero'),
                   ('ot','Amistoso')],
        required=True,        
    )
    
    organizacion_que_representa = fields.Char(
        string='Organización que representa ese tripulante',
        required=True,
    )
    
    manifiesto = fields.Char(
        string='Manifiesto',
        readonly=True,
        store=False
        
    )    
    
    aceptar_manifiesto = fields.Selection(
        string='Aceptar Manifiesto',
        selection=[('1', 'Si'), ('0', 'No')],
        required=True,
        help='Estoy de acuerdo con las condiciones del Manifiesto de la Nave'
    )
    
    observaciones = fields.Char(
        string='Observaciones',
    )
    
    
    
    
    