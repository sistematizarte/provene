# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 

# wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
# tar -xvf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz 
# sudo cp ./wkhtmltox/bin/wkhtmltoimage /usr/bin/
# sudo cp ./wkhtmltox/bin/wkhtmltopdf /usr/bin/
# sudo apt-get install zlib1g fontconfig libxrender1 libfreetype6 libxext6 libx11-6

from odoo import models, fields, api
# from bs4 import BeautifulSoup
# from odoo.exceptions import ValidationError
# import requests
import psycopg2
import logging
import pytz


_logger = logging.getLogger(__name__)

list_ = []

class TransaccionLaNave(models.Model): 
    _name = 'provene.transaccion.bd'
    
    def _fecha_hora_creacion(self):
        try:
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)  
            context_today = pytz.utc.localize(fields.Datetime.now()).astimezone(user_tz)
            return context_today.strftime("%d/%m/%Y %H:%M:%S")
            _logger.info('........................................................................... 1003 %s' % ( fields.Date.context_today(self).strftime("%d/%m/%Y %H:%M:%S")))
        except:
            return 0
            _logger.info('........................................................................... 3 %s' % ('Error al intentar colocar la fecha de Sincronización'))
    

    name = fields.Char(
        string='Fecha de Sincronización de las Bases de Datos',
        default=_fecha_hora_creacion,
        required=True
    )
    
    modelo_transaccion = fields.Char(string='Modelo de la Transacción', 
        required=True
    )
    
    metodo_transaccion = fields.Char(string='Método de la Transacción', 
        required=True
    )
    
    registro_id = fields.Char(
        string='Número identificador del Registro',
    )

    values_transaccion = fields.Char(string='Valores de la Transacción', 
        required=True
    )
    
    transaccion_sincronizada = fields.Boolean(string='Transacción está Sincronizada', 
        required=True
    )
    
    values_transaccion_backup = fields.Char(string='Valores de Respaldo de la Transacción')
    
    transaccion_id = fields.Char(
        string='Número identificador de este registro',
    )
    