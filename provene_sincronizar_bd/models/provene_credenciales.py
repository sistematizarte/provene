# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 

# wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
# tar -xvf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz 
# sudo cp ./wkhtmltox/bin/wkhtmltoimage /usr/bin/
# sudo cp ./wkhtmltox/bin/wkhtmltopdf /usr/bin/
# sudo apt-get install zlib1g fontconfig libxrender1 libfreetype6 libxext6 libx11-6

from odoo import models, fields, api
# from odoo.exceptions import ValidationError
import psycopg2
import logging
import pytz


_logger = logging.getLogger(__name__)

list_ = []

class CredencialesLaNave(models.Model): 
    _name = 'provene.credenciales'
    
    def _fecha_hora_creacion(self):
        try:
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)  
            context_today = pytz.utc.localize(fields.Datetime.now()).astimezone(user_tz)
            return context_today.strftime("%d/%m/%Y %H:%M:%S")
            _logger.info('........................................................................... 1003 %s' % ( fields.Date.context_today(self).strftime("%d/%m/%Y %H:%M:%S")))
        except:
            return 0
            _logger.info('........................................................................... 3 %s' % ('Error al intentar colocar la fecha de Sincronización'))
    
    # 0.1
    def mostrar_resultados_update(self):
        list_.append('Inicio de la función # 0.1 << mostrar_resultados_update >>')        
        aux = ''
        i = 1
        for li in list_:
            print(li)
            aux =  aux + '<p>' + str(i) + ': ' + li + '</p>'
            i = i + 1
        self.resultados_update = aux
        list_.append('Salió de la función << mostrar_resultados_update >>')
        
        list_.clear()

    estatus = fields.Selection([('activo', 'Activo'), ('inactivo', 'Inactivo')],string='Estado de estas credenciales', default='inactivo')
    
    # Campos del servidor
    name = fields.Char(string='IP HOST SERVER',required=True, placeholder = '192.168.0.1')
    database_server = fields.Char(string='NAME DATABASE SERVER', required= True, placeholder = 'nave_db')
    user_db_server = fields.Char(string='USER DB SERVER', required=True, placeholder = 'userdb')
    password_db_server = fields.Char(string='PASSWORD DB SERVER',required=True, placeholder = 'lanave')
    user_server = fields.Char(string='USER SERVER', required=True, placeholder = 'user@example.com')
    password_server = fields.Char(string='PASSWORD SERVER', required=True, placeholder = '0000')
    port_server = fields.Char(string='PORT SERVER',required=True, placeholder = '80')

    # Campos locales
    host_local = fields.Char(string='IP HOST LOCAL',required=True, placeholder = '192.168.0.1')
    database_local = fields.Char(string='NAME DATABASE LOCAL', required= True, placeholder = 'nave_db')
    user_db_local = fields.Char(string='USER DB LOCAL', required=True, placeholder = 'userdb')
    password_db_local = fields.Char(string='PASSWORD DB LOCAL',required=True, placeholder = 'lanave')
    user_local = fields.Char(string='USER LOCAL', required=True, placeholder = 'user@example.com')
    password_local = fields.Char(string='PASSWORD LOCAL', required=True, placeholder = '0000')
    port_local = fields.Char(string='PORT LOCAL',required=True, placeholder = '80')
  
    