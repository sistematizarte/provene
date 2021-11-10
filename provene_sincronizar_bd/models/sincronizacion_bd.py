# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 

# wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
# tar -xvf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz 
# sudo cp ./wkhtmltox/bin/wkhtmltoimage /usr/bin/
# sudo cp ./wkhtmltox/bin/wkhtmltopdf /usr/bin/
# sudo apt-get install zlib1g fontconfig libxrender1 libfreetype6 libxext6 libx11-6

# ESTE ES EL QUE FUNCIONA REALMENTE------------------------------------------------------v
# sudo apt update
# sudo apt install xfonts-75dpi xfonts-base gvfs colord glew-utils libvisual-0.4-plugins gstreamer1.0-tools opus-tools qt5-image-formats-plugins qtwayland5 qt5-qmltooling-plugins librsvg2-bin lm-sensors
# sudo wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.stretch_amd64.deb
# sudo dpkg -i wkhtmltox_0.12.5-1.stretch_amd64.deb
# sudo cp /usr/local/bin/wkhtmltopdf /usr/bin/
# sudo cp /usr/local/bin/wkhtmltoimage /usr/bin/

# Then running:
# wkhtmltopdf -V

# Returns:
# wkhtmltopdf 0.12.5 (with patched qt)

# ESTE ES EL QUE FUNCIONA REALMENTE------------------------------------------------------^


from odoo import models, fields, api
# from bs4 import BeautifulSoup
# from odoo.exceptions import ValidationError
# import requests
import psycopg2
import logging
import pytz
import odoorpc
import ast
import datetime

_logger = logging.getLogger(__name__)

list_ = []

class SincronizarBD(models.Model): 
    _name = 'provene.sincronizar.bd'
    
    # HOST_SERVER="34.68.236.125"
    # DATABASE_SERVER="bitnami_odoo"
    # USER_SERVER="postgres"
    # PASSWORD_SERVER="gmWC3QAUudPC"
    # PORT_SERVER = 80
    
    # HOST_LOCAL="127.0.0.1"
    # DATABASE_LOCAL="provene_local_6_1"
    # USER_LOCAL="openpg"
    # PASSWORD_LOCAL="openpgpwd"
    
    HOST_SERVER= False
    DATABASE_SERVER= False
    USER_BD_SERVER= False
    PASSWORD_BD_SERVER= False
    USER_SERVER= False
    PASSWORD_SERVER= False
    PORT_SERVER = False
    
    HOST_LOCAL= False
    DATABASE_LOCAL= False
    USER_BD_LOCAL= False
    PASSWORD_BD_LOCAL= False
    USER_LOCAL= False
    PASSWORD_LOCAL= False
    PORT_LOCAL = False
    
    #  para instalar la funcion dblink en base de datos
    
    def get_fecha_hora(self):
        try:
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)  
            context_today = pytz.utc.localize(fields.Datetime.now()).astimezone(user_tz)
            _logger.info('........................................................................... 1003 %s' % ( fields.Date.context_today(self).strftime("%d/%m/%Y %H:%M:%S")))
            return context_today.strftime("%d/%m/%Y %H:%M:%S")
        except Exception as exc:
            list_.append('Error: %s' % (exc))
            _logger.info('........................................................................... 3 %s' % (exc))
    
    def restar_hora(self,hora1,hora2):
        formato = '%d/%m/%Y %H:%M:%S'
        h1 = datetime.datetime.strptime(hora1,formato)
        h2 = datetime.datetime.strptime(hora2,formato)
        resultado = h1 - h2
        return str(resultado)
    
    # 0.0 - BCREATE EXTENSION dblink
    def cargar_credenciales_bajada(self):
        NOMBRE_TABLA = 'public.provene_credenciales'
        NOMBRE_FUNCION = 'cargar_credenciales_bajada'
        
        list_.append('Inicio de la función # 0.0 - B << %s >>' % (NOMBRE_FUNCION))
        reg = {}
        reg_id = self.env['provene.credenciales'].search([('estatus','=','activo')],order='write_date desc',limit=1)
        if len(reg_id) > 0:
            reg= self.env['provene.credenciales'].browse(reg_id.id)
            list_.append('Credenciales activas: << %s >>' % (reg))
            for s in reg:
                self.HOST_SERVER=s.name
                self.DATABASE_SERVER=s.database_server
                self.USER_BD_SERVER=s.user_db_server
                self.PASSWORD_BD_SERVER=s.password_db_server
                self.USER_SERVER=s.user_server
                self.PASSWORD_SERVER=s.password_server
                self.PORT_SERVER = s.port_server

                self.HOST_LOCAL= s.host_local
                self.DATABASE_LOCAL= s.database_local
                self.USER_BD_LOCAL= s.user_db_local
                self.PASSWORD_BD_LOCAL=s.password_db_local
                self.USER_LOCAL= s.user_local
                self.PASSWORD_LOCAL= s.password_local
                self.PORT_LOCAL = s.port_local
                
                _logger.info("""Credenciales...................... 228 \t\t\t\t {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12} {13} \t\t\t\t 
                             """.format(self.HOST_SERVER,
                                        self.DATABASE_SERVER,
                                        self.USER_BD_SERVER,
                                        self.PASSWORD_BD_SERVER,
                                        self.USER_SERVER,
                                        self.PASSWORD_SERVER,
                                        self.PORT_SERVER ,
                                        self.HOST_LOCAL,
                                        self.DATABASE_LOCAL,
                                        self.USER_BD_LOCAL,
                                        self.PASSWORD_BD_LOCAL,
                                        self.USER_LOCAL,
                                        self.PASSWORD_LOCAL,
                                        self.PORT_LOCAL ,))
            
            return True
        else:
            list_.append('No hay credenciales activas')
            return False
    
    # 0.0 - S
    def cargar_credenciales_subida(self):
        NOMBRE_TABLA = 'public.provene_credenciales'
        NOMBRE_FUNCION = 'cargar_credenciales_subida'
        
        list_.append('Inicio de la función # 0.0 - S << %s >>' % (NOMBRE_FUNCION))
        reg = {}
        reg_id = self.env['provene.credenciales'].search([('estatus','=','activo')],order='write_date desc',limit=1)
        if len(reg_id) > 0:
            reg= self.env['provene.credenciales'].browse(reg_id.id)
            list_.append('Credenciales activas: << %s >>' % (reg))
            for s in reg:
                self.HOST_SERVER = s.host_local
                self.DATABASE_SERVER = s.database_local
                self.USER_BD_SERVER = s.user_db_local
                self.PASSWORD_BD_SERVER = s.password_db_local
                self.USER_SERVER = s.user_local
                self.PASSWORD_SERVER = s.password_local
                self.PORT_SERVER = s.port_local

                self.HOST_LOCAL = s.name
                self.DATABASE_LOCAL = s.database_server
                self.USER_BD_LOCAL = s.user_db_server
                self.PASSWORD_BD_LOCAL = s.password_db_server
                self.USER_LOCAL = s.user_server
                self.PASSWORD_LOCAL = s.password_server
                self.PORT_LOCAL = s.port_server



                _logger.info("""Credenciales...................... 228 \t\t\t\t {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12} {13} \t\t\t\t 
                             """.format(self.HOST_SERVER,
                                        self.DATABASE_SERVER,
                                        self.USER_BD_SERVER,
                                        self.PASSWORD_BD_SERVER,
                                        self.USER_SERVER,
                                        self.PASSWORD_SERVER,
                                        self.PORT_SERVER ,
                                        self.HOST_LOCAL,
                                        self.DATABASE_LOCAL,
                                        self.USER_BD_LOCAL,
                                        self.PASSWORD_BD_LOCAL,
                                        self.USER_LOCAL,
                                        self.PASSWORD_LOCAL,
                                        self.PORT_LOCAL ,))
            
            return True
        else:
            list_.append('No hay credenciales activas')
            return False
            
        
        
    #- TABLAS PARA USUARIOS 1.0----------------------------------------------------------------------------------------------
    # 1.0
    def submenu_usuarios(self):
        self.name = self.get_fecha_hora()
        self.estatus = '1'
        NOMBRE_FUNCION = 'submenu_usuarios'
        list_.append('Inicio de la función # 1.0 << %s >>' % (NOMBRE_FUNCION))
        credenciales = self.cargar_credenciales_bajada()
        if credenciales:
            self.action_bajar_usuarios()
        # self.mostrar_resultados_update()
        list_.append('Fin de la función # 1.0 << %s >>' % (NOMBRE_FUNCION))
        self.name_fin = self.get_fecha_hora()
        self.tiempo_transcurrido = str(self.restar_hora(self.name_fin,self.name))
    
    # 1.1 - A
    def action_bajar_usuarios(self):
        NOMBRE_TABLA = 'public.res_users'
        # NOMBRE_TABLA_REAL = 'public.registro_asesoria_registro_cuestionario1_c21_rel'
        NOMBRE_FUNCION = 'action_bajar_usuarios'
        list_.append('Inicio de la función # 1.1 - A << %s >>' % (NOMBRE_FUNCION))

        try:
            conexion = psycopg2.connect(host=self.HOST_LOCAL, database=self.DATABASE_LOCAL, user=self.USER_BD_LOCAL, password=self.PASSWORD_BD_LOCAL)  
            cur = conexion.cursor()

            sql = """  	SELECT	T2.ID_G,
								T2.NAME_G,
								T2.NAME,
                                T2.LANG,
                                T2.id ,
                                T2.login ,
                                T2.company_id ,
                                T2.partner_id ,
                                T2.create_date,
                                T2.signature, 
                                T2.action_id, 
                                T2.share, 
                                T2.create_uid, 
                                T2.write_uid,
                                T2.write_date, 
                                T2.alias_id, 
                                T2.notification_type , 
                                T2.out_of_office_message, 
                                T2.odoobot_state , 
                                T2.telefono, 
                                T2.tipo_tripulante, 
                                T2.aceptar_manifiesto,
                                T2.organizacion_que_representa,
                                T2.observaciones,
                                T2.password
                        FROM    dblink( 'host={0} dbname={1} user={2} password={3}', 
                                        'select id ,
                                                active ,
                                                login ,
                                                password,
                                                company_id ,
                                                partner_id ,
                                                create_date,
                                                signature, 
                                                action_id, 
                                                share, 
                                                create_uid, 
                                                write_uid,
                                                write_date
                                                FROM res_users
                                                WHERE id NOT BETWEEN 1 AND 5
                                                order by id')	AS t1(	id integer ,
                                                                        active boolean ,
                                                                        login varchar ,
                                                                        password varchar,
                                                                        company_id integer ,
                                                                        partner_id integer ,
                                                                        create_date timestamp ,
                                                                        signature varchar, 
                                                                        action_id integer, 
                                                                        share boolean, 
                                                                        create_uid integer, 
                                                                        write_uid integer,
                                                                        write_date timestamp)
                        RIGHT JOIN
    						dblink( 'host={4} dbname={5} user={6} password={7}',  
                                    'select RG.ID,
                                    		RG.name,
					    					RP.NAME,
                                            RP.LANG,
                                            RU.partner_id ,
                                            RU.active ,
                                            RU.login ,
                                            RU.password,
                                            RU.company_id ,
                                            RU.partner_id ,
                                            RU.create_date,
                                            RU.signature, 
                                            RU.action_id, 
                                            RU.share, 
                                            RU.create_uid, 
                                            RU.write_uid,
                                            RU.write_date, 
                                            RU.alias_id, 
                                            RU.notification_type , 
                                            RU.out_of_office_message, 
                                            RU.odoobot_state , 
                                            RU.telefono, 
                                            RU.tipo_tripulante, 
                                            RU.aceptar_manifiesto,
                                            RU.organizacion_que_representa,
                                            RU.observaciones
                                            FROM res_users RU, res_partner RP, res_groups_users_rel RGU, res_groups RG
                                            WHERE 	RU.partner_id = RP.ID
						AND RG.ID = RGU.gid
						AND RU.ID = RGU.uid
						AND (RG.name like ''%Ajustes%'' OR RG.name like ''%Capit%'')
                                                AND RU.id NOT BETWEEN 1 AND 5
                                            order by RU.id')	AS t2(	id_g integer ,
																	name_g varchar,
																	name varchar,
                                                                    lang varchar,
                                                                    id integer ,
                                                                    active boolean ,
                                                                    login varchar ,
                                                                    password varchar,
                                                                    company_id integer ,
                                                                    partner_id integer ,
                                                                    create_date timestamp ,
                                                                    signature varchar, 
                                                                    action_id integer, 
                                                                    share boolean, 
                                                                    create_uid integer, 
                                                                    write_uid integer,
                                                                    write_date timestamp , 
                                                                    alias_id integer, 
                                                                    notification_type varchar , 
                                                                    out_of_office_message varchar, 
                                                                    odoobot_state varchar , 
                                                                    telefono varchar, 
                                                                    tipo_tripulante varchar, 
                                                                    aceptar_manifiesto varchar,
                                                                    organizacion_que_representa varchar,
                                                                    observaciones varchar  )
                        ON T1.login = T2.login
                        WHERE T1.login IS NULL 
                                """.format(self.HOST_LOCAL,self.DATABASE_LOCAL,self.USER_BD_LOCAL,self.PASSWORD_BD_LOCAL
                                          ,self.HOST_SERVER,self.DATABASE_SERVER,self.USER_BD_SERVER,self.PASSWORD_BD_SERVER)
            _logger.info('SQL action_bajar_usuarios........................................................................... 222 \t\t\t\t %s \t\t\t\t ' % (sql))
            cur.execute(sql)
            if cur.rowcount > 0:
                list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %(NOMBRE_TABLA))
                
                usuarios = cur.fetchall()
                values = []
                grupos = []
                for usuario in usuarios:
                    if usuario[0] == 15:
                        permiso_acceso = True
                        creacion_contactos = True
                        capitan_tripulante = 'in_group_' + str((self.env['res.groups'].search([('name','like','%Capitán%')],limit=1)).id)
                        grupos.append('%s' % (capitan_tripulante))

                        _logger.info('capitan_tripulante........................................................................... 20 \t\t\t\t %s \t\t\t\t ' % (capitan_tripulante))
                    else:
                        permiso_acceso = False
                        capitan_tripulante = 'in_group_' + str((self.env['res.groups'].search([('name','like','%Tripulante%')],limit=1)).id)
                        grupos.append('%s' % (capitan_tripulante))
                        _logger.info('capitan_tripulante........................................................................... 30 \t\t\t\t %s \t\t\t\t ' % (capitan_tripulante))
                        creacion_contactos = False

                    # password_real = usuario[24] if usuario[24] else ''
                    values.append({
                        'name': usuario[2],
                        'telefono': usuario[19],
                        'tipo_tripulante': usuario[20],
                        'login': usuario[5],
                        'lang': usuario[3],
                        'write_date': usuario[14],
                        'sel_groups_1_8_9':1,
                        'in_group_2':permiso_acceso,
                        capitan_tripulante:True,
                        'in_group_7':creacion_contactos,
                        # 'password':password_real,
                        'organizacion_que_representa':usuario[22],
                        'aceptar_manifiesto':usuario[21],
                        'observaciones':usuario[23]
                    })
                    # list_.append('values: %s ----- %s' % (values, cur.statusmessage))
                    # list_.append('values: %s ----- ' % (values))
                _logger.info('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t %s' % (values, cur.statusmessage))

                record = self.env['res.users'].create(values)
                list_.append('Grupos para cada registro %s ' % (grupos))
                list_.append('Se crearon %s nuevos registros con ids: %s' % (len(record),record))
                _logger.info('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t ' % (record))
                list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
                # self.action_actualizar_claves_usuarios()
                # self.reenmplazar_password()
            else:
                list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            # _logger.info('Casos Legales........................................................................... 1 %s' % (cur.statusmessage))
            # self.mostrar_resultados_update()
                
        except (Exception, psycopg2.DatabaseError) as error:
            list_.append('Error: (%s). Al intentar insertar en la tabla << %s >> en la función action_bajar_casos_legal' %(error, NOMBRE_TABLA))
            _logger.info('Que carajo hace esto con los values........................................................................... 3 %s' % (error))
        finally:
            cur.close()
            conexion.close()  		

    # 1.1 - B.1
    def action_actualizar_claves_usuarios(self):
        NOMBRE_TABLA = 'public.res_users'
        # NOMBRE_TABLA_REAL = 'public.registro_asesoria_registro_cuestionario1_c21_rel'
        NOMBRE_FUNCION = 'action_actualizar_claves_usuarios'
        list_.append('Inicio de la función # 1.1 - B.1 << %s >>' % (NOMBRE_FUNCION))

        try:
            conexion = psycopg2.connect(host=self.HOST_LOCAL, database=self.DATABASE_LOCAL, user=self.USER_BD_LOCAL, password=self.PASSWORD_BD_LOCAL)  
            cur = conexion.cursor()
            # cur = self.env.cr
            sql = """   SELECT  id ,
                                active ,
                                login ,
                                password,
                                company_id ,
                                partner_id ,
                                create_date,
                                signature, 
                                action_id, 
                                share, 
                                create_uid, 
                                write_uid,
                                write_date, 
                                alias_id, 
                                notification_type , 
                                out_of_office_message, 
                                odoobot_state , 
                                telefono, 
                                tipo_tripulante, 
                                aceptar_manifiesto,
                                organizacion_que_representa,
                                observaciones
                                
                        FROM 	dblink( 'host=%s dbname=%s user=%s password=%s',  
                                        'select id ,
                                                active ,
                                                login ,
                                                password,
                                                company_id ,
                                                partner_id ,
                                                create_date,
                                                signature, 
                                                action_id, 
                                                share, 
                                                create_uid, 
                                                write_uid,
                                                write_date, 
                                                alias_id, 
                                                notification_type , 
                                                out_of_office_message, 
                                                odoobot_state , 
                                                telefono, 
                                                tipo_tripulante, 
                                                aceptar_manifiesto,
                                                organizacion_que_representa,
                                                observaciones
                                        FROM res_users
                                        WHERE id NOT BETWEEN 1 AND 5
                                        order by id'
                                        )
                                        AS t2(id integer ,
                                            active boolean ,
                                            login varchar ,
                                            password varchar,
                                            company_id integer ,
                                            partner_id integer ,
                                            create_date timestamp ,
                                            signature varchar, 
                                            action_id integer, 
                                            share boolean, 
                                            create_uid integer, 
                                            write_uid integer,
                                            write_date timestamp , 
                                            alias_id integer, 
                                            notification_type varchar , 
                                            out_of_office_message varchar, 
                                            odoobot_state varchar , 
                                            telefono varchar, 
                                            tipo_tripulante varchar, 
                                            aceptar_manifiesto varchar,
                                            organizacion_que_representa varchar,
                                            observaciones varchar)
                                """ % (self.HOST_SERVER,self.DATABASE_SERVER,self.USER_BD_SERVER,self.PASSWORD_BD_SERVER)
            cur.execute(sql)
            if cur.rowcount > 0:
                list_.append('La consulta encontró en la tabla << %s >> %s registros en el servidor que aún no estan en la PC local' %(NOMBRE_TABLA,cur.rowcount))
                
                campo_actualizar = cur.fetchall()
                descripcion = cur.description
                logins = []
                for update_casos_legal in campo_actualizar:
                    i = 0
                    
                    sql = ' UPDATE res_users SET '
                    for cd in descripcion:
                        if i == 3:
                            # Unicamente Actualiza la Clave de Usuario
                            sql = sql + cd.name + '=\'%s\' ' % (update_casos_legal[i])
                        i=i+1
                    sql = sql + ' WHERE login=\'%s\' ' % (update_casos_legal[2])
                    cur.execute(sql)
                    # list_.append('Comentar Línea, SQL que construyó para modificar la tabla %s: \t\n %s \t\n' %(NOMBRE_TABLA, sql))
                    # list_.append('Registros que coinciden ---------------------->>>>>>>>>>>>>>>%s \n' %(cur.rowcount))
                    if cur.rowcount > 0:
                        conexion.commit()
                        # list_.append('Se actualizó el registro [login: %s] de la tabla << %s >> en la PC local (%s)' %(update_casos_legal[2],NOMBRE_TABLA,cur.statusmessage))
                        logins.append('[login: {0}] ({1})'.format(update_casos_legal[2],cur.statusmessage))
                        _logger.info('........................................................................... 1 %s TABLA %s en la funcion: %s' % (cur.statusmessage,NOMBRE_TABLA, NOMBRE_FUNCION))
                    else:
                        logins.append('[login: {0}] ({1})'.format(update_casos_legal[2],cur.statusmessage))
                        _logger.info('........................................................................... 2 %s TABLA %s en la funcion: %s' % (cur.statusmessage,NOMBRE_TABLA, NOMBRE_FUNCION))
                        list_.append('No hubo actualización en la tabla << %s >> de la PC local  para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                
                list_.append('Se actualizaron los registros [%s] de la tabla << %s >> en la PC local' %(logins,NOMBRE_TABLA))
                list_.append('------------------------------------------------------------------------------------------------------------')
            else:
                _logger.info('........................................................................... 2 %s' % (cur.statusmessage))
                list_.append('La consulta NO encontró diferencias entre la tabla << %s >> del Servidor y la PC local (%s)' %(NOMBRE_TABLA,cur.statusmessage))			
                
        except (Exception, psycopg2.DatabaseError) as error:
            list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA,NOMBRE_FUNCION))
            _logger.info('........................................................................... 3 %s TABLA %s en la funcion: %s' % (error,NOMBRE_TABLA, NOMBRE_FUNCION))
        finally:
            cur.close()
            conexion.close()     
    
    # 1.1 - B.2
    def reenmplazar_password(self):
        NOMBRE_TABLA = 'public.res_users'
        NOMBRE_FUNCION = 'reenmplazar_password'
        list_.append('Inicio de la función # 1.1 - B.2 << %s >>' % (NOMBRE_FUNCION))
        
        try:
            conexion = psycopg2.connect(host=self.HOST_LOCAL, database=self.DATABASE_LOCAL, user=self.USER_BD_LOCAL, password=self.PASSWORD_BD_LOCAL)  
            cur = conexion.cursor()
            # cur = self.env.cr
            sql = """   SELECT  id ,
                                active ,
                                login ,
                                password,
                                company_id ,
                                partner_id ,
                                create_date,
                                signature, 
                                action_id, 
                                share, 
                                create_uid, 
                                write_uid,
                                write_date, 
                                alias_id, 
                                notification_type , 
                                out_of_office_message, 
                                odoobot_state , 
                                telefono, 
                                tipo_tripulante, 
                                aceptar_manifiesto
                        FROM 	dblink( 'host=%s dbname=%s user=%s password=%s',  
                                        'select id ,
                                                active ,
                                                login ,
                                                password,
                                                company_id ,
                                                partner_id ,
                                                create_date,
                                                signature, 
                                                action_id, 
                                                share, 
                                                create_uid, 
                                                write_uid,
                                                write_date, 
                                                alias_id, 
                                                notification_type , 
                                                out_of_office_message, 
                                                odoobot_state , 
                                                telefono, 
                                                tipo_tripulante, 
                                                aceptar_manifiesto
                                        FROM res_users
                                        WHERE id NOT BETWEEN 1 AND 5
                                        order by id'
                                        )
                                        AS t2(id integer ,
                                            active boolean ,
                                            login varchar ,
                                            password varchar,
                                            company_id integer ,
                                            partner_id integer ,
                                            create_date timestamp ,
                                            signature varchar, 
                                            action_id integer, 
                                            share boolean, 
                                            create_uid integer, 
                                            write_uid integer,
                                            write_date timestamp , 
                                            alias_id integer, 
                                            notification_type varchar , 
                                            out_of_office_message varchar, 
                                            odoobot_state varchar , 
                                            telefono varchar, 
                                            tipo_tripulante varchar, 
                                            aceptar_manifiesto varchar)
                   
                                """ % (self.HOST_SERVER,self.DATABASE_SERVER,self.USER_BD_SERVER,self.PASSWORD_BD_SERVER)
            cur.execute(sql)
            if cur.rowcount > 0:
                list_.append('La consulta encontró en la tabla << %s >>, %s registros en el servidor que aún no estan en la PC local' %(NOMBRE_TABLA,cur.rowcount))
                
                campo_actualizar = cur.fetchall()
                descripcion = cur.description
                logins = []
                for update_casos_legal in campo_actualizar:
                    i = 0
                    
                    sql = 'UPDATE  res_users SET '
                    for cd in descripcion:
                        if i == 3:
                            # Unicamente Actualiza la Clave de Usuario
                            sql = sql + cd.name + '=\'%s\'' % ('$pbkdf2-sha512$25000$BoCQ0nrvnROitJYy5tw7pw$cAS2mp5kyN.sD9rx09orY9BRNKIrT1HZnr2L8aBLiaun81frC3Fxlu8QRFtkJDB4pv0rqw75nOVgQqBDY8CeXQ')
                        i=i+1
                    sql = sql + ' WHERE login=\'%s\' ' % (update_casos_legal[2])
                    cur.execute(sql)
                    # list_.append('Comentar Línea, SQL que construyó para modificar la tabla %s: \n %s \n' %(NOMBRE_TABLA, sql))
                    # list_.append('Registros que coinciden ---------------------->>>>>>>>>>>>>>>%s \n' %(cur.rowcount))
                    if cur.rowcount > 0:
                        conexion.commit()
                        # list_.append('Se actualizó el registro [login: %s] de la tabla << %s >> en la PC local (%s)' %(update_casos_legal[2],NOMBRE_TABLA,cur.statusmessage))
                        logins.append('[login: {0}] ({1})'.format(update_casos_legal[2],cur.statusmessage))
                        _logger.info('........................................................................... 1 %s TABLA %s en la funcion: %s' % (cur.statusmessage,NOMBRE_TABLA, NOMBRE_FUNCION))
                    else: 
                        # _logger.info('........................................................................... 2 %s TABLA %s en la funcion: %s' % (cur.statusmessage,NOMBRE_TABLA, NOMBRE_FUNCION))
                        logins.append('[login: {0}] ({1})'.format(update_casos_legal[2],cur.statusmessage))
                        list_.append('No hubo actualización el registro [login: %s] en la tabla << %s >> de la PC local  para este caso (%s)' %(update_casos_legal[2],NOMBRE_TABLA,cur.statusmessage))
                list_.append('Se actualizaron los registros [%s] de la tabla << %s >> en la PC local' %(logins,NOMBRE_TABLA))
                list_.append('------------------------------------------------------------------------------------------------------------')
            else:
                _logger.info('........................................................................... 2 %s' % (cur.statusmessage))
                list_.append('La consulta NO encontró diferencias entre la tabla << %s >> del Servidor y la PC local (%s)' %(NOMBRE_TABLA,cur.statusmessage))			
                
        except (Exception, psycopg2.DatabaseError) as error:
            list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA,NOMBRE_FUNCION))
            _logger.info('........................................................................... 3 %s TABLA %s en la funcion: %s' % (error,NOMBRE_TABLA, NOMBRE_FUNCION))
        except Exception as exc:
            list_.append('Error: %s' % (exc))

    def reenmplazar_password_up(self):
        NOMBRE_TABLA = 'public.res_users'
        NOMBRE_FUNCION = 'reenmplazar_password'
        list_.append('Inicio de la función # 1.1 - B.2 << %s >>' % (NOMBRE_FUNCION))

        try:
            conexion = psycopg2.connect(host=self.HOST_LOCAL, database=self.DATABASE_LOCAL, user=self.USER_BD_LOCAL,
                                        password=self.PASSWORD_BD_LOCAL)
            cur = conexion.cursor()
            conexion_local = psycopg2.connect(host=self.HOST_SERVER, database=self.DATABASE_SERVER, user=self.USER_BD_SERVER,
                                        password=self.PASSWORD_BD_SERVER)
            cur_local = conexion_local.cursor()
            # cur = self.env.cr
            sql = """   select id ,
                                                active ,
                                                login ,
                                                password,
                                                company_id ,
                                                partner_id ,
                                                create_date,
                                                signature, 
                                                action_id, 
                                                share, 
                                                create_uid, 
                                                write_uid,
                                                write_date, 
                                                alias_id, 
                                                notification_type , 
                                                out_of_office_message, 
                                                odoobot_state , 
                                                telefono, 
                                                tipo_tripulante, 
                                                aceptar_manifiesto
                                        FROM res_users
                                        WHERE id NOT BETWEEN 1 AND 5
                                        order by id
                                        
                                """
            cur_local.execute(sql)
            if cur_local.rowcount > 0:
                list_.append(
                    'La consulta encontró en la tabla << %s >>, %s registros en el servidor que aún no estan en la PC local' % (
                    NOMBRE_TABLA, cur_local.rowcount))

                campo_actualizar = cur_local.fetchall()
                descripcion = cur_local.description
                logins = []
                for update_casos_legal in campo_actualizar:
                    i = 0

                    sql = 'UPDATE  res_users SET '
                    for cd in descripcion:
                        if i == 3:
                            # Unicamente Actualiza la Clave de Usuario
                            sql = sql + cd.name + '=\'%s\'' % (
                                '$pbkdf2-sha512$25000$BoCQ0nrvnROitJYy5tw7pw$cAS2mp5kyN.sD9rx09orY9BRNKIrT1HZnr2L8aBLiaun81frC3Fxlu8QRFtkJDB4pv0rqw75nOVgQqBDY8CeXQ')
                        i = i + 1
                    sql = sql + ' WHERE login=\'%s\' ' % (update_casos_legal[2])
                    cur.execute(sql)
                    # list_.append('Comentar Línea, SQL que construyó para modificar la tabla %s: \n %s \n' %(NOMBRE_TABLA, sql))
                    # list_.append('Registros que coinciden ---------------------->>>>>>>>>>>>>>>%s \n' %(cur.rowcount))
                    if cur.rowcount > 0:
                        conexion.commit()
                        # list_.append('Se actualizó el registro [login: %s] de la tabla << %s >> en la PC local (%s)' %(update_casos_legal[2],NOMBRE_TABLA,cur.statusmessage))
                        logins.append('[login: {0}] ({1})'.format(update_casos_legal[2], cur.statusmessage))
                        _logger.info(
                            '........................................................................... 1 %s TABLA %s en la funcion: %s' % (
                            cur.statusmessage, NOMBRE_TABLA, NOMBRE_FUNCION))
                    else:
                        # _logger.info('........................................................................... 2 %s TABLA %s en la funcion: %s' % (cur.statusmessage,NOMBRE_TABLA, NOMBRE_FUNCION))
                        logins.append('[login: {0}] ({1})'.format(update_casos_legal[2], cur.statusmessage))
                        list_.append(
                            'No hubo actualización el registro [login: %s] en la tabla << %s >> de la PC local  para este caso (%s)' % (
                            update_casos_legal[2], NOMBRE_TABLA, cur.statusmessage))
                list_.append(
                    'Se actualizaron los registros [%s] de la tabla << %s >> en la PC local' % (logins, NOMBRE_TABLA))
                list_.append(
                    '------------------------------------------------------------------------------------------------------------')
            else:
                _logger.info('........................................................................... 2 %s' % (
                    cur.statusmessage))
                list_.append(
                    'La consulta NO encontró diferencias entre la tabla << %s >> del Servidor y la PC local (%s)' % (
                    NOMBRE_TABLA, cur.statusmessage))

        except (Exception, psycopg2.DatabaseError) as error:
            list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función %s' % (
            error, NOMBRE_TABLA, NOMBRE_FUNCION))
            _logger.info(
                '........................................................................... 3 %s TABLA %s en la funcion: %s' % (
                error, NOMBRE_TABLA, NOMBRE_FUNCION))
        except Exception as exc:
            list_.append('Error: %s' % (exc))



    #- TABLAS DE APOYO 2.0----------------------------------------------------------------------------------------------
    # 2.0
    def submenu_apoyo(self):
        NOMBRE_FUNCION = 'submenu_apoyo'
        list_.append('Inicio de la función # 2.0 << %s >>' % (NOMBRE_FUNCION))
        self.action_descargar_instruccion_valor()
        self.action_descargar_asesoria_valor()
        self.action_descargar_manifiesto_valor()
        self.action_descargar_directorio_valor()
        self.action_descargar_registro_cs2()
        self.action_descargar_registro_cs4()
        self.action_descargar_registro_cs6()
        self.action_descargar_registro_cs9()
        self.action_descargar_registro_cuestionario1_c19()
        self.action_descargar_registro_cuestionario1_c21()
        list_.append('Fin de la función # 2.0 << %s >>' % (NOMBRE_FUNCION))
        
    # 2.1
    def action_descargar_instruccion_valor(self):

        NOMBRE_TABLA = 'public.instruccion_valor'
        NOMBRE_FUNCION = 'action_descargar_instruccion_valor'
        list_.append('Inicio de la función # 2.1 << %s >>' % (NOMBRE_FUNCION))

        try:
            conexion = psycopg2.connect(host=self.HOST_LOCAL, database=self.DATABASE_LOCAL, user=self.USER_BD_LOCAL, password=self.PASSWORD_BD_LOCAL)  
            cur = conexion.cursor()
            sql = 'DELETE FROM %s ' % (NOMBRE_TABLA)
            cur.execute(sql)
            # conexion.commit()
            list_.append('Se limpió la tabla << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            
            sql = """ 	INSERT INTO %s
                        SELECT *
                        FROM 	dblink( 'host=%s dbname=%s user=%s password=%s', 
                                        'SELECT id ,
                                                instruccion_valor, 
                                                requisito_documento, 
                                                "Procedimiento_documento", 
                                                create_uid,
                                                create_date, 
                                                write_uid, 
                                                write_date 
                                        FROM instruccion_valor
                                        ORDER BY id')
                            AS t2(	id integer ,
                                instruccion_valor varchar, 
                                requisito_documento varchar, 
                                Procedimiento_documento varchar, 
                                create_uid integer,
                                create_date timestamp, 
                                write_uid integer, 
                                write_date timestamp )
                                    """ % (NOMBRE_TABLA
                                          ,self.HOST_SERVER,self.DATABASE_SERVER,self.USER_BD_SERVER,self.PASSWORD_BD_SERVER)
            cur.execute(sql)
            if cur.rowcount > 0:
                conexion.commit()
                list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
            else:
                list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
        except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar insertar registros la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA, NOMBRE_FUNCION))
        finally:
            cur.close()
            conexion.close()
    
    # 2.2
    def action_descargar_asesoria_valor(self):
        
        NOMBRE_TABLA = 'public.asesoria_valor'
        NOMBRE_FUNCION = 'action_descargar_asesoria_valor'

        list_.append('Inicio de la función # 2.2 << %s >>' % (NOMBRE_FUNCION))
        
        # HOST_LOCAL="127.0.0.1"
        # DATABASE_LOCAL="provene_local_6"
        # USER_LOCAL="openpg"
        # PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=self.HOST_LOCAL, database=self.DATABASE_LOCAL, user=self.USER_BD_LOCAL, password=self.PASSWORD_BD_LOCAL)  
            cur = conexion.cursor()
            sql = 'DELETE FROM %s ' % (NOMBRE_TABLA)
            cur.execute(sql)
            list_.append('Se limpió la tabla << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            
            sql = """ 	INSERT INTO %s
                        SELECT *
                        FROM 	dblink( 'host=%s dbname=%s user=%s password=%s', 
                                        'SELECT id ,
                                            asesoria_valor,
                                            create_uid,
                                            create_date, 
                                            write_uid, 
                                            write_date 
                                        FROM asesoria_valor
                                        ORDER BY id')
                                AS t2(	id integer ,
                                    asesoria_valor varchar, 
                                    create_uid integer,
                                    create_date timestamp, 
                                    write_uid integer, 
                                    write_date timestamp ) 
                        """ % (NOMBRE_TABLA
                              ,self.HOST_SERVER,self.DATABASE_SERVER,self.USER_BD_SERVER,self.PASSWORD_BD_SERVER)
            cur.execute(sql)
            if cur.rowcount > 0:
                conexion.commit()
                list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
            else:
                list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
        except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar insertar registros la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA, NOMBRE_FUNCION))
        finally:
            cur.close()
            conexion.close()

    # 2.3
    def action_descargar_manifiesto_valor(self):
        
        NOMBRE_TABLA = 'public.manifiesto_valor'
        NOMBRE_FUNCION = 'action_descargar_manifiesto_valor'

        list_.append('Inicio de la función # 2.3 << %s >>' % (NOMBRE_FUNCION))
        
        # HOST_LOCAL="127.0.0.1"
        # DATABASE_LOCAL="provene_local_6"
        # USER_LOCAL="openpg"
        # PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=self.HOST_LOCAL, database=self.DATABASE_LOCAL, user=self.USER_BD_LOCAL, password=self.PASSWORD_BD_LOCAL)  
            cur = conexion.cursor()
            sql = 'DELETE FROM %s ' % (NOMBRE_TABLA)
            cur.execute(sql)
            list_.append('Se limpió la tabla << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            
            sql = """ 	INSERT INTO %s
                        SELECT *
                        FROM 	dblink( 'host=%s dbname=%s user=%s password=%s', 
                                        'SELECT id ,
                                            manifiesto_nombre,
                                            manifiesto_valor,
                                            create_uid,
                                            create_date, 
                                            write_uid, 
                                            write_date
                                        FROM manifiesto_valor
                                        ORDER BY id')
                                AS t2(	id integer ,
                                    manifiesto_nombre varchar,
                                    manifiesto_valor varchar, 
                                    create_uid integer,
                                    create_date timestamp, 
                                    write_uid integer, 
                                    write_date timestamp ) 
                            """ % (NOMBRE_TABLA
                                  ,self.HOST_SERVER,self.DATABASE_SERVER,self.USER_BD_SERVER,self.PASSWORD_BD_SERVER)
            cur.execute(sql)
            if cur.rowcount > 0:
                conexion.commit()
                list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
            else:
                list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
        except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar insertar registros la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA, NOMBRE_FUNCION))
        finally:
            cur.close()
            conexion.close()

    # 2.4
    def action_descargar_directorio_valor(self):
        
        NOMBRE_TABLA = 'public.directorio_valor'
        NOMBRE_FUNCION = 'action_descargar_directorio_valor'

        list_.append('Inicio de la función # 2.4 << %s >>' % (NOMBRE_FUNCION))
        
        # HOST_LOCAL="127.0.0.1"
        # DATABASE_LOCAL="provene_local_6"
        # USER_LOCAL="openpg"
        # PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=self.HOST_LOCAL, database=self.DATABASE_LOCAL, user=self.USER_BD_LOCAL, password=self.PASSWORD_BD_LOCAL)  
            cur = conexion.cursor()
            sql = 'DELETE FROM %s ' % (NOMBRE_TABLA)
            cur.execute(sql)
            list_.append('Se limpió la tabla << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            
            sql = """ 	INSERT INTO %s
                        SELECT *
                        FROM 	dblink( 'host=%s dbname=%s user=%s password=%s',
                                        'SELECT id ,
                                                directorio_valor,
                                                parroquia,
                                                municipio,
                                                estado,
                                                nacionalidad,
                                                direccion_institucion,
                                                create_uid,
                                                create_date, 
                                                write_uid, 
                                                write_date 
                                        FROM directorio_valor
                                        ORDER BY id')
                                AS t2(	id integer ,
                                    directorio_valor varchar, 
                                    nacionalidad integer,
                                    parroquia integer,
                                    municipio integer,
                                    estado integer,
                                    direccion_institucion varchar, 
                                    create_uid integer,
                                    create_date timestamp, 
                                    write_uid integer, 
                                    write_date timestamp ) 
                                    """ % (NOMBRE_TABLA
                                          ,self.HOST_SERVER,self.DATABASE_SERVER,self.USER_BD_SERVER,self.PASSWORD_BD_SERVER)
            cur.execute(sql)
            if cur.rowcount > 0:
                conexion.commit()
                list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
            else:
                list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
        except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar insertar registros la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA, NOMBRE_FUNCION))
        finally:
            cur.close()
            conexion.close()

    # 2.5
    def action_descargar_registro_cs2(self):
        
        NOMBRE_TABLA = 'public.registro_cs2'
        NOMBRE_FUNCION = 'action_descargar_registro_cs2'

        list_.append('Inicio de la función # 2.5 << %s >>' % (NOMBRE_FUNCION))
        
        # HOST_LOCAL="127.0.0.1"
        # DATABASE_LOCAL="provene_local_6"
        # USER_LOCAL="openpg"
        # PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=self.HOST_LOCAL, database=self.DATABASE_LOCAL, user=self.USER_BD_LOCAL, password=self.PASSWORD_BD_LOCAL)  
            cur = conexion.cursor()
            sql = 'DELETE FROM %s ' % (NOMBRE_TABLA)
            cur.execute(sql)
            list_.append('Se limpió la tabla << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            
            sql = """ 	INSERT INTO %s
                        SELECT *
                        FROM 	dblink(  'host=%s dbname=%s user=%s password=%s',
                                'SELECT id ,
                                        cs2_actividad_asistencia,
                                        cont_cs2,
                                        create_uid,
                                        create_date, 
                                        write_uid, 
                                        write_date 
                                FROM registro_cs2
                                ORDER BY id')
                        AS t2(	id integer ,
                            cs2_actividad_asistencia varchar, 
                            cont_cs2 integer,
                            create_uid integer,
                            create_date timestamp, 
                            write_uid integer, 
                            write_date timestamp ) """ % (NOMBRE_TABLA
                                                         ,self.HOST_SERVER,self.DATABASE_SERVER,self.USER_BD_SERVER,self.PASSWORD_BD_SERVER)
            cur.execute(sql)
            if cur.rowcount > 0:
                conexion.commit()
                list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
            else:
                list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
        except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar insertar registros la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA, NOMBRE_FUNCION))
        finally:
            cur.close()
            conexion.close()

    # 2.6
    def action_descargar_registro_cs4(self):
        
        NOMBRE_TABLA = 'public.registro_cs4'
        NOMBRE_FUNCION = 'action_descargar_registro_cs4'

        list_.append('Inicio de la función # 2.6 << %s >>' % (NOMBRE_FUNCION))
        
        # HOST_LOCAL="127.0.0.1"
        # DATABASE_LOCAL="provene_local_6"
        # USER_LOCAL="openpg"
        # PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=self.HOST_LOCAL, database=self.DATABASE_LOCAL, user=self.USER_BD_LOCAL, password=self.PASSWORD_BD_LOCAL)  
            cur = conexion.cursor()
            sql = 'DELETE FROM %s ' % (NOMBRE_TABLA)
            cur.execute(sql)
            list_.append('Se limpió la tabla << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            
            sql = """ 	INSERT INTO %s
                        SELECT *
                        FROM 	dblink( 'host=%s dbname=%s user=%s password=%s',
                                'SELECT id ,
                                        cs4_tribunales,
                                        cont_cs4,
                                        create_uid,
                                        create_date, 
                                        write_uid, 
                                        write_date 
                                FROM registro_cs4
                                ORDER BY id')
                        AS t2(	id integer ,
                            cs4_tribunales varchar,
                            cont_cs4 integer, 
                            create_uid integer,
                            create_date timestamp, 
                            write_uid integer, 
                            write_date timestamp ) """ % (NOMBRE_TABLA
                                                         ,self.HOST_SERVER,self.DATABASE_SERVER,self.USER_BD_SERVER,self.PASSWORD_BD_SERVER)
            cur.execute(sql)
            if cur.rowcount > 0:
                conexion.commit()
                list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
            else:
                list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
        except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar insertar registros la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA, NOMBRE_FUNCION))
        finally:
            cur.close()
            conexion.close()

    # 2.7
    def action_descargar_registro_cs6(self):
        
        NOMBRE_TABLA = 'public.registro_cs6'
        NOMBRE_FUNCION = 'action_descargar_registro_cs6'

        list_.append('Inicio de la función # 2.7 << %s >>' % (NOMBRE_FUNCION))
        
        # HOST_LOCAL="127.0.0.1"
        # DATABASE_LOCAL="provene_local_6"
        # USER_LOCAL="openpg"
        # PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=self.HOST_LOCAL, database=self.DATABASE_LOCAL, user=self.USER_BD_LOCAL, password=self.PASSWORD_BD_LOCAL)  
            cur = conexion.cursor()
            sql = 'DELETE FROM %s ' % (NOMBRE_TABLA)
            cur.execute(sql)
            list_.append('Se limpió la tabla << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            
            sql = """ 	INSERT INTO %s
                        SELECT *
                        FROM 	dblink( 'host=%s dbname=%s user=%s password=%s', 
                                'SELECT id ,
                                        cs6_no_contribuir,
                                        cont_cs6,
                                        create_uid,
                                        create_date, 
                                        write_uid, 
                                        write_date 
                                FROM registro_cs6
                                ORDER BY id')
                        AS t2(	id integer ,
                            cs6_no_contribuir varchar,
                            cont_cs6 integer,
                            create_uid integer,
                            create_date timestamp, 
                            write_uid integer, 
                            write_date timestamp ) """ % (NOMBRE_TABLA
                                                         ,self.HOST_SERVER,self.DATABASE_SERVER,self.USER_BD_SERVER,self.PASSWORD_BD_SERVER)
            cur.execute(sql)
            if cur.rowcount > 0:
                conexion.commit()
                list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
            else:
                list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
        except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar insertar registros la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA, NOMBRE_FUNCION))
        finally:
            cur.close()
            conexion.close()

    # 2.8
    def action_descargar_registro_cs9(self):
        
        NOMBRE_TABLA = 'public.registro_cs9'
        NOMBRE_FUNCION = 'action_descargar_registro_cs9'

        list_.append('Inicio de la función # 2.8 << %s >>' % (NOMBRE_FUNCION))
        
        # HOST_LOCAL="127.0.0.1"
        # DATABASE_LOCAL="provene_local_6"
        # USER_LOCAL="openpg"
        # PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=self.HOST_LOCAL, database=self.DATABASE_LOCAL, user=self.USER_BD_LOCAL, password=self.PASSWORD_BD_LOCAL)  
            cur = conexion.cursor()
            sql = 'DELETE FROM %s ' % (NOMBRE_TABLA)
            cur.execute(sql)
            list_.append('Se limpió la tabla << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            
            sql = """ 	INSERT INTO %s
                        SELECT *
                        FROM 	dblink( 'host=%s dbname=%s user=%s password=%s', 
                                'SELECT id ,
                                        cs9_expectativas,
                                        cont_cs9,
                                        create_uid,
                                        create_date, 
                                        write_uid, 
                                        write_date 
                                FROM registro_cs9
                                ORDER BY id')
                        AS t2(	id integer ,
                            cs9_expectativas varchar, 
                            cont_cs9 integer,
                            create_uid integer,
                            create_date timestamp, 
                            write_uid integer, 
                            write_date timestamp ) """ % (NOMBRE_TABLA
                                                        ,self.HOST_SERVER,self.DATABASE_SERVER,self.USER_BD_SERVER,self.PASSWORD_BD_SERVER)
            cur.execute(sql)
            if cur.rowcount > 0:
                conexion.commit()
                list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
            else:
                list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
        except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar insertar registros la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA, NOMBRE_FUNCION))
        finally:
            cur.close()
            conexion.close()

    # 2.9
    def action_descargar_registro_cuestionario1_c19(self):
    
        NOMBRE_TABLA = 'public.registro_cuestionario1_c19'
        NOMBRE_FUNCION = 'action_descargar_registro_cuestionario1_c19'

        list_.append('Inicio de la función # 2.9 << %s >>' % (NOMBRE_FUNCION))
        
        # HOST_LOCAL="127.0.0.1"
        # DATABASE_LOCAL="provene_local_6"
        # USER_LOCAL="openpg"
        # PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=self.HOST_LOCAL, database=self.DATABASE_LOCAL, user=self.USER_BD_LOCAL, password=self.PASSWORD_BD_LOCAL)  
            cur = conexion.cursor()
            sql = 'DELETE FROM %s ' % (NOMBRE_TABLA)
            cur.execute(sql)
            list_.append('Se limpió la tabla << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            
            sql = """ 	INSERT INTO %s
                        SELECT *
                        FROM 	dblink( 'host=%s dbname=%s user=%s password=%s', 
                                'SELECT id ,
                                        c19_beneficios_estado,
                                        cont_c19,
                                        create_uid,
                                        create_date, 
                                        write_uid, 
                                        write_date 
                                FROM registro_cuestionario1_c19
                                ORDER BY id')
                        AS t2(	id integer ,
                            c19_beneficios_estado varchar,
                            cont_c19 integer, 
                            create_uid integer,
                            create_date timestamp, 
                            write_uid integer, 
                            write_date timestamp ) """ % (NOMBRE_TABLA
                                                         ,self.HOST_SERVER,self.DATABASE_SERVER,self.USER_BD_SERVER,self.PASSWORD_BD_SERVER)
            cur.execute(sql)
            if cur.rowcount > 0:
                conexion.commit()
                list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
            else:
                list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
        except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar insertar registros la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA, NOMBRE_FUNCION))
        finally:
            cur.close()
            conexion.close()

    # 2.10
    def action_descargar_registro_cuestionario1_c21(self):
        
        NOMBRE_TABLA = 'public.registro_cuestionario1_c21'
        NOMBRE_FUNCION = 'action_descargar_registro_cuestionario1_c21'

        list_.append('Inicio de la función # 2.10 << %s >>' % (NOMBRE_FUNCION))
        
        # HOST_LOCAL="127.0.0.1"
        # DATABASE_LOCAL="provene_local_6"
        # USER_LOCAL="openpg"
        # PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=self.HOST_LOCAL, database=self.DATABASE_LOCAL, user=self.USER_BD_LOCAL, password=self.PASSWORD_BD_LOCAL)  
            cur = conexion.cursor()
            sql = 'DELETE FROM %s ' % (NOMBRE_TABLA)
            cur.execute(sql)
            list_.append('Se limpió la tabla << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            
            sql = """ 	INSERT INTO %s
                        SELECT *
                        FROM 	dblink( 'host=%s dbname=%s user=%s password=%s', 
                                'SELECT id ,
                                        c21_principal_problema,
                                        cont_c21,
                                        create_uid,
                                        create_date, 
                                        write_uid, 
                                        write_date 
                                FROM registro_cuestionario1_c21
                                ORDER BY id')
                        AS t2(	id integer ,
                            c21_principal_problema varchar, 
                            cont_c21 integer,
                            create_uid integer,
                            create_date timestamp, 
                            write_uid integer, 
                            write_date timestamp ) """ % (NOMBRE_TABLA
                                                         ,self.HOST_SERVER,self.DATABASE_SERVER,self.USER_BD_SERVER,self.PASSWORD_BD_SERVER)
            cur.execute(sql)
            if cur.rowcount > 0:
                conexion.commit()
                list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
            else:
                list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
        except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar insertar registros la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA, NOMBRE_FUNCION))
        finally:
            cur.close()
            conexion.close()

    #- TABLAS PARA LAS TRANSACCIONES 3.0----------------------------------------------------------------------------------------------
    # 3.1
    def verificar_coincidencias(self):
        
        NOMBRE_TABLA = 'public.provene_transaccion_bd'
        # NOMBRE_TABLA_REAL = 'public.registro_asesoria_registro_cuestionario1_c21_rel'
        NOMBRE_FUNCION = 'verificar_coincidencias'
        list_.append('Inicio de la función # 3.1 << %s >>' % (NOMBRE_FUNCION))

        id_coincidente = []

        try:
            conexion = psycopg2.connect(host=self.HOST_LOCAL, database=self.DATABASE_LOCAL, user=self.USER_BD_LOCAL, password=self.PASSWORD_BD_LOCAL)       
            cur = conexion.cursor()
            # cur2 = conexion.cursor()
            # cr = self.env.cr
            sql = """  	SELECT	t2.id 
                        FROM  	dblink( 'host=%s dbname=%s user=%s password=%s', 
                                        'SELECT id ,
                                                transaccion_id
                                        FROM provene_transaccion_bd') AS t1(id integer,
                                                                            transaccion_id character varying )
                        RIGHT JOIN 
                                dblink( 'host=%s dbname=%s user=%s password=%s',  
                                        'SELECT id ,
                                                transaccion_id
                                        FROM provene_transaccion_bd') AS t2(id integer,
                                                                            transaccion_id character varying )
                        ON T1.transaccion_id = T2.transaccion_id
                        WHERE T1.transaccion_id IS NULL
                        ORDER BY T2.ID
                                """  % (self.HOST_LOCAL,self.DATABASE_LOCAL,self.USER_BD_LOCAL,self.PASSWORD_BD_LOCAL
                                       ,self.HOST_SERVER,self.DATABASE_SERVER,self.USER_BD_SERVER,self.PASSWORD_BD_SERVER)
            cur.execute(sql)
            if cur.rowcount > 0:
                for id_coincidentes in cur.fetchall():
                    id_coincidente.append(id_coincidentes[0])
                list_.append("Se actualizarán en la Nave Local %s registros << %s >>" % (cur.rowcount,NOMBRE_TABLA))
            else:
                list_.append("¡La Nave esta totalmente actualizada! (%s)" % (cur.statusmessage))
            return id_coincidente
        except (Exception, psycopg2.DatabaseError) as error:
            list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA,NOMBRE_FUNCION))
            # _logger.info('........................................................................... 3 %s TABLA %s en la funcion: %s' % (error,NOMBRE_TABLA, NOMBRE_FUNCION))
        except Exception as exc:
            list_.append('Error: %s' % (exc))

    def verificar_coincidencias_up(self):

        NOMBRE_TABLA = 'public.provene_transaccion_bd'
        # NOMBRE_TABLA_REAL = 'public.registro_asesoria_registro_cuestionario1_c21_rel'
        NOMBRE_FUNCION = 'verificar_coincidencias'
        list_.append('Inicio de la función # 3.1 << %s >>' % (NOMBRE_FUNCION))

        id_coincidente = []

        try:
            #conexion = psycopg2.connect(host=self.HOST_LOCAL, database=self.DATABASE_LOCAL, user=self.USER_BD_LOCAL,
                                        #password=self.PASSWORD_BD_LOCAL)
            conexion = psycopg2.connect(host=self.HOST_SERVER, database=self.DATABASE_SERVER, user=self.USER_BD_SERVER,
                                        password=self.PASSWORD_BD_SERVER)
            cur = conexion.cursor()
            # cur2 = conexion.cursor()
            # cr = self.env.cr
            sql = """  	SELECT	t2.id 
                        FROM  	dblink( 'host=%s dbname=%s user=%s password=%s', 
                                        'SELECT id ,
                                                transaccion_id
                                        FROM provene_transaccion_bd') AS t1(id integer,
                                                                            transaccion_id character varying )
                        RIGHT JOIN 
                                (SELECT id ,
                                                transaccion_id
                                        FROM provene_transaccion_bd) AS T2
                        ON T1.transaccion_id = T2.transaccion_id
                        WHERE T1.transaccion_id IS NULL
                        ORDER BY T2.ID
                                """ % (self.HOST_LOCAL, self.DATABASE_LOCAL, self.USER_BD_LOCAL, self.PASSWORD_BD_LOCAL)
            cur.execute(sql)
            if cur.rowcount > 0:
                for id_coincidentes in cur.fetchall():
                    id_coincidente.append(id_coincidentes[0])
                list_.append("Se actualizarán en la Nave Local %s registros << %s >>" % (cur.rowcount, NOMBRE_TABLA))
            else:
                list_.append("¡La Nave esta totalmente actualizada! (%s)" % (cur.statusmessage))
            return id_coincidente
        except (Exception, psycopg2.DatabaseError) as error:
            list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función %s' % (
            error, NOMBRE_TABLA, NOMBRE_FUNCION))
            # _logger.info('........................................................................... 3 %s TABLA %s en la funcion: %s' % (error,NOMBRE_TABLA, NOMBRE_FUNCION))
        except Exception as exc:
            list_.append('Error: %s' % (exc))

    # 3.2
    def sincronizar_transacciones(self,accion):
        
        NOMBRE_FUNCION = 'sincronizar_transacciones'
        list_.append('Inicio de la función # 3.2 << %s >>' % (NOMBRE_FUNCION))
    
        HOST_SERVER = self.HOST_SERVER
        DATABASE_SERVER = self.DATABASE_SERVER
        USER_SERVER = self.USER_SERVER
        PASSWORD_SERVER = self.PASSWORD_SERVER
        PORT_SERVER  = self.PORT_SERVER

        HOST_LOCAL = self.HOST_LOCAL
        DATABASE_LOCAL = self.DATABASE_LOCAL
        USER_LOCAL = self.USER_LOCAL
        PASSWORD_LOCAL = self.PASSWORD_LOCAL
        PORT_LOCAL  = self.PORT_LOCAL

        # HOST_SERVER="127.0.0.1"
        # DATABASE_SERVER="provene_local_6_1"
        # # DATABASE_SERVER="provene_local_6"
        # USER_SERVER="user@example.com"
        # PASSWORD_SERVER="1234"
        # PORT_SERVER = 8069

        # HOST_LOCAL="127.0.0.1"
        # DATABASE_LOCAL="provene_local_6"
        # # DATABASE_LOCAL="provene_local_6_1"
        # USER_LOCAL="user@example.com"
        # PASSWORD_LOCAL="1234"
        # PORT_LOCAL = 8069

        odoo_s = odoorpc.ODOO(HOST_SERVER, port=PORT_SERVER)
        # odoo_l = odoorpc.ODOO(HOST_LOCAL, port=PORT_LOCAL)
        odoo_user = odoorpc.ODOO(HOST_LOCAL, port=PORT_LOCAL)

        # Login
        odoo_s.login(DATABASE_SERVER, USER_SERVER,PASSWORD_SERVER )
        # odoo_l.login(DATABASE_LOCAL, USER_LOCAL,PASSWORD_LOCAL )

        user_data = odoo_s.env['provene.transaccion.bd']
        # registros = user_data.search([('transaccion_sincronizada','=',False)])
        registros = self.verificar_coincidencias() if accion ==1 else self.verificar_coincidencias_up()
        campos = user_data.browse(registros)

        for value in campos:
            try:
                ejecutar = True
                values = ast.literal_eval(value.values_transaccion)
                modelo = str(value.modelo_transaccion)
                metodo = str(value.metodo_transaccion)
        
                if metodo == 'create':
                    registros_s = odoo_s.execute('res.users', 'read', int(value.create_uid.id))[0]
                if metodo == 'write' or metodo == 'unlink':
                    registros_s = odoo_s.execute('res.users', 'read', int(value.write_uid.id))[0]

                login_s = registros_s['login']
                print(login_s)

                odoo_user.login(DATABASE_LOCAL, login_s,PASSWORD_LOCAL )
            
                if metodo == 'create':
                    modelo_s = odoo_s.env[modelo]

                    if modelo == 'registro.asesoria':
                        jornada_s = odoo_s.execute(modelo, 'read', ast.literal_eval(value.registro_id))
                        values['datos_jornada_calendario'] = jornada_s[0]['datos_jornada_calendario']
                        if not value.transaccion_id:
                            transaccion_id = values['cedula'] + datetime.datetime.now().strftime("%d%m%Y%H%M%S%f")
                            transaccion_id_s = {'transaccion_id':transaccion_id}
                            cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, transaccion_id_s)
                        else:
                            transaccion_id_s = {'transaccion_id':value.transaccion_id}
                    if modelo == 'registro.asesoria.calendario':
                        registros_s_ = odoo_s.execute('res.users', 'read', values['tripulante_usuario'][0][2])
                        logins = []
                        for registro_login in registros_s_:
                            logins.append(registro_login['login'])
                        if len(registros_s_) > 0:
                            id_l_l = odoo_user.env['res.users'].search([('login','in',logins)])
                            values['tripulante_usuario'] = [[6,False,id_l_l]]
                            if not value.transaccion_id:
                                # transaccion_id = values['name'] + values['tipo_actividad'] + str(pytz.utc.localize(fields.Datetime.now()).astimezone(pytz.timezone(self.env.context.get('tz') or self.env.user.tz)).strftime("%d%m%Y%H%M%S"))
                                transaccion_id = values['name'] + values['tipo_actividad'] + datetime.datetime.now().strftime("%d%m%Y%H%M%S%f")
                                transaccion_id_s = {'transaccion_id':transaccion_id}
                                cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, transaccion_id_s)
                            else:
                                transaccion_id_s = {'transaccion_id':value.transaccion_id}
                    if modelo == 'registro.pasajeros.actividad.social':
                        actividad_area_social_s = odoo_s.execute('registro.actividad.social', 'read', values['actividad_id'])
                        registro_asesoria_calendario_s = odoo_s.execute('registro.asesoria.calendario', 'read', actividad_area_social_s[0]['actividad_area_social'][0])[0]
                        
                        modelo_l = odoo_user.env['registro.asesoria.calendario'].search([('name','=',registro_asesoria_calendario_s['name']),('tipo_actividad','=',registro_asesoria_calendario_s['tipo_actividad'])])
                        if len(modelo_l) > 0:
                            for id_l in modelo_l:
                                id_l_l = odoo_user.env['registro.actividad.social'].search([('actividad_area_social','=',id_l)])[0]
                                values['actividad_id'] = id_l_l
                                if not value.transaccion_id:
                                    transaccion_id = values['cedula'] + str(values['actividad_id']) + datetime.datetime.now().strftime("%d%m%Y%H%M%S%f")
                                    transaccion_id_s = {'transaccion_id':transaccion_id}
                                    cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, transaccion_id_s)
                                else:
                                    transaccion_id_s = {'transaccion_id':value.transaccion_id}
                                # cedula_l = odoo_user.execute(modelo, 'write', id_l, values)
                                list_.append('Se modificó el registro %s la tabla << %s >> con el método %s' % (id_l_l,modelo,metodo))
                        else:
                            ejecutar = False
                    if modelo == 'casos.legal':
                        jornada_s = odoo_s.execute(modelo, 'read', ast.literal_eval(value.registro_id))
                        values['datos_jornada_calendario'] = jornada_s[0]['datos_jornada_calendario']
            
                        registros_s_ = odoo_s.execute('res.users', 'read', int(values['tripulante_asignado']))[0]
                        login_s_ = registros_s_['login']
                        if len(login_s_) > 0:
                            id_l_l = odoo_user.env['res.users'].search([('login','=',login_s_)])[0]
                            values['tripulante_asignado'] = id_l_l
                            # values_transaccion_s = {'values_transaccion':values}
                            if not value.transaccion_id:
                                transaccion_id = values['cedula'] + values['datos_jornada_calendario'] + values['categoria_area_legal'] + datetime.datetime.now().strftime("%d%m%Y%H%M%S%f")
                                transaccion_id_s = {'transaccion_id':transaccion_id}
                                cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, transaccion_id_s)
                            else:
                                transaccion_id_s = {'transaccion_id':value.transaccion_id}
                        else:
                            ejecutar = False
            
                    if ejecutar:
                        resulado = odoo_user.execute(modelo, metodo, values)
                        list_.append('Se creó el registro %s la tabla << %s >> con el metodo %s' % (resulado,modelo,metodo))
                        id_l_t = odoo_user.env['provene.transaccion.bd'].search([],order='write_date desc',limit=1)
                        odoo_user.execute('provene.transaccion.bd', 'write', id_l_t, transaccion_id_s)

                
                if metodo == 'write':
                    modelo_s = odoo_s.env[modelo]
                    cedula_s = odoo_s.execute(modelo, 'read', ast.literal_eval(value.registro_id))
            
                    modelo_l = odoo_user.env[modelo]
                    if modelo == 'registro.asesoria':
                        modelo_l = modelo_l.search([('cedula','=',cedula_s[0]['cedula'])])
                        registro_modelo = cedula_s[0]['cedula']
                        if not value.transaccion_id:
                                transaccion_id = cedula_s[0]['cedula'] + datetime.datetime.now().strftime("%d%m%Y%H%M%S%f")
                                transaccion_id_s = {'transaccion_id':transaccion_id}
                                cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, transaccion_id_s)
                        else:
                            transaccion_id_s = {'transaccion_id':value.transaccion_id}

            
                    if modelo == 'registro.asesoria.calendario':
                        if 'tripulante_usuario' in values:
                            registros_s_ = odoo_s.execute('res.users', 'read', values['tripulante_usuario'][0][2])
                            logins = []
                            for registro_login in registros_s_:
                                logins.append(registro_login['login'])
                            if len(registros_s_) > 0:
                                id_l_l = odoo_user.env['res.users'].search([('login','in',logins)])
                                values['tripulante_usuario'] = [[6,False,id_l_l]]
                                # values_transaccion_s = {'values_transaccion':values}
                                # cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, values_transaccion_s)
                        modelo_l = modelo_l.search([('name','=',cedula_s[0]['name']),('tipo_actividad','=',cedula_s[0]['tipo_actividad'])])
                        registro_modelo = cedula_s[0]['name']
                        if not value.transaccion_id:
                            transaccion_id = cedula_s[0]['name'] + cedula_s[0]['tipo_actividad'] + datetime.datetime.now().strftime("%d%m%Y%H%M%S%f")
                            transaccion_id_s = {'transaccion_id':transaccion_id}
                            cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, transaccion_id_s)
                        else:
                            transaccion_id_s = {'transaccion_id':value.transaccion_id}
            
                    if modelo == 'registro.pasajeros.actividad.social':
                        actividad_area_social_s = odoo_s.execute('registro.actividad.social', 'read', cedula_s[0]['actividad_id'][0])
                        registro_asesoria_calendario_s = odoo_s.execute('registro.asesoria.calendario', 'read', actividad_area_social_s[0]['actividad_area_social'][0])[0]
                        
                        modelo_l_ = odoo_user.env['registro.asesoria.calendario'].search([('name','=',registro_asesoria_calendario_s['name']),('tipo_actividad','=',registro_asesoria_calendario_s['tipo_actividad'])])
                        if len(modelo_l_) > 0:
                            for id_l in modelo_l_:
                                id_l_l = odoo_user.env['registro.actividad.social'].search([('actividad_area_social','=',id_l)])[0]
                                list_.append('Se modificó el registro %s la tabla << %s >> con el método %s' % (id_l_l,modelo,metodo))
                                modelo_l = modelo_l.search([('cedula','=',cedula_s[0]['cedula']),('actividad_id','=',id_l_l)])
                                registro_modelo = cedula_s[0]['cedula']
                                if not value.transaccion_id:
                                    transaccion_id = cedula_s[0]['cedula'] + str(cedula_s[0]['actividad_id'][0]) + datetime.datetime.now().strftime("%d%m%Y%H%M%S%f")
                                    transaccion_id_s = {'transaccion_id':transaccion_id}
                                    cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, transaccion_id_s)
                                else:
                                    transaccion_id_s = {'transaccion_id':value.transaccion_id}
            
                    if modelo == 'casos.legal':
                        if 'tripulante_asignado' in values:
                            registros_s_ = odoo_s.execute('res.users', 'read', int(values['tripulante_asignado']))[0]
                            login_s_ = registros_s_['login']
                            if len(login_s_) > 0:
                                id_l_l = odoo_user.env['res.users'].search([('login','=',login_s_)])[0]
                                values['tripulante_asignado'] = id_l_l
                                values_transaccion_s = {'values_transaccion':values}
                                cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, values_transaccion_s)
                            
                        # 	list_.append('Se modificó el registro %s la tabla << %s >> con el método %s' % (id_l_l,modelo,metodo))
                        modelo_l = modelo_l.search(['&','&',('cedula','=',cedula_s[0]['cedula']),('datos_jornada_calendario','=',cedula_s[0]['datos_jornada_calendario']),('categoria_area_legal','=',cedula_s[0]['categoria_area_legal'])])
                        registro_modelo = cedula_s[0]['cedula']
                        if not value.transaccion_id:
                            transaccion_id = cedula_s[0]['cedula'] + cedula_s[0]['datos_jornada_calendario'] + cedula_s[0]['categoria_area_legal'] + datetime.datetime.now().strftime("%d%m%Y%H%M%S%f")
                            transaccion_id_s = {'transaccion_id':transaccion_id}
                            cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, transaccion_id_s)
                        else:
                            transaccion_id_s = {'transaccion_id':value.transaccion_id}

                    if len(modelo_l) > 0:
                        for id_l in modelo_l:
                            cedula_l = odoo_user.execute(modelo, 'write', id_l, values)
                            list_.append('Se modificó el registro %s la tabla << %s >> con el metodo %s' % (registro_modelo,modelo,metodo))
                            id_l_t = odoo_user.env['provene.transaccion.bd'].search([],order='write_date desc',limit=1)
                            # values_transaccion_s_t = {'transaccion_id':str(value.values_transaccion_backup)}
                            odoo_user.execute('provene.transaccion.bd', 'write', id_l_t, transaccion_id_s)
                    else:
                        list_.append('No se puedo modificar el registro %s en la tabla << %s >> para poder aplicar el método %s' % (registro_modelo,modelo,metodo))
                
                if metodo == 'unlink':
                    modelo_l = odoo_user.env[modelo]
                    if modelo == 'registro.asesoria':
                        modelo_l = modelo_l.search([('cedula','=',values['cedula'].strip())])
                        registro_modelo = values['cedula']
                        if not value.transaccion_id:
                            transaccion_id = values['cedula'] + datetime.datetime.now().strftime("%d%m%Y%H%M%S%f")
                            transaccion_id_s = {'transaccion_id':transaccion_id}
                            cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, transaccion_id_s)
                        else:
                            transaccion_id_s = {'transaccion_id':value.transaccion_id}
            
                    if modelo == 'registro.asesoria.calendario':
                        modelo_l = modelo_l.search([('name','=',values['name']),('tipo_actividad','=',values['tipo_actividad'])])
                        registro_modelo = values['name']
                        if not value.transaccion_id:
                            # transaccion_id = values['name'] + values['tipo_actividad'] + str(pytz.utc.localize(fields.Datetime.now()).astimezone(pytz.timezone(self.env.context.get('tz') or self.env.user.tz)).strftime("%d%m%Y%H%M%S"))
                            transaccion_id = values['name'] + values['tipo_actividad'] + datetime.datetime.now().strftime("%d%m%Y%H%M%S%f")
                            transaccion_id_s = {'transaccion_id':transaccion_id}
                            cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, transaccion_id_s)
                        else:
                            transaccion_id_s = {'transaccion_id':value.transaccion_id}
            
                    if modelo == 'registro.pasajeros.actividad.social':
                        actividad_area_social_s = odoo_s.execute('registro.actividad.social', 'read', ast.literal_eval(values['actividad_id']))
                        registro_asesoria_calendario_s = odoo_s.execute('registro.asesoria.calendario', 'read', actividad_area_social_s[0]['actividad_area_social'][0])[0]
                        
                        modelo_l_ = odoo_user.env['registro.asesoria.calendario'].search([('name','=',registro_asesoria_calendario_s['name']),('tipo_actividad','=',registro_asesoria_calendario_s['tipo_actividad'])])
                        if len(modelo_l_) > 0:
                            for id_l in modelo_l_:
                                id_l_l = odoo_user.env['registro.actividad.social'].search([('actividad_area_social','=',id_l)])[0]
                                list_.append('Se modificó el registro %s la tabla << %s >> con el método %s' % (id_l_l,modelo,metodo))
                                modelo_l = modelo_l.search([('cedula','=',values['cedula']),('actividad_id','=',id_l_l)])
                                registro_modelo = values['cedula']
                                if not value.transaccion_id:
                                    transaccion_id = values['cedula'] + str(values['actividad_id']) + datetime.datetime.now().strftime("%d%m%Y%H%M%S%f")
                                    transaccion_id_s = {'transaccion_id':transaccion_id}
                                    cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, transaccion_id_s)
                                else:
                                    transaccion_id_s = {'transaccion_id':value.transaccion_id}
            
                    if modelo == 'casos.legal':
                        # 	list_.append('Se modificó el registro %s la tabla << %s >> con el método %s' % (id_l_l,modelo,metodo))
                        modelo_l = modelo_l.search(['&','&',('cedula','=',values['cedula']),('datos_jornada_calendario','=',values['datos_jornada_calendario']),('categoria_area_legal','=',values['categoria_area_legal'])])
                        registro_modelo = values['cedula']
                        if not value.transaccion_id:
                            transaccion_id = values['cedula'] + values['datos_jornada_calendario'] + values['categoria_area_legal'] + datetime.datetime.now().strftime("%d%m%Y%H%M%S%f")
                            transaccion_id_s = {'transaccion_id':transaccion_id}
                            cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, transaccion_id_s)
                        else:
                            transaccion_id_s = {'transaccion_id':value.transaccion_id}
            
                    if len(modelo_l) > 0:
                        for cedula_ in modelo_l:
                            cedula_l = odoo_user.execute(modelo, 'unlink', cedula_)
                            list_.append('Se eliminó el registro %s la tabla << %s >> con el metodo %s' % (registro_modelo,modelo,metodo))
                            id_l_t = odoo_user.env['provene.transaccion.bd'].search([],order='write_date desc',limit=1)
                            # values_transaccion_s_t = {'transaccion_id':str(value.values_transaccion_backup)}
                            odoo_user.execute('provene.transaccion.bd', 'write', id_l_t, transaccion_id_s)
                    else:
                        list_.append('No se puedo eliminar el registro %s en la tabla << %s >> para poder aplicar el método %s' % (registro_modelo,modelo,metodo))
                
                odoo_user.logout()	
        
            except odoorpc.error.Error as exc:
                list_.append('Error: %s' % (exc.info))
            except odoorpc.error.InternalError as exc:
                list_.append('Error: %s' % (exc.info))
            except odoorpc.error.RPCError as exc:
                list_.append('Error: %s' % (exc.info))
            except Exception as exc:
                list_.append('Error: %s' % (exc))
        odoo_s.logout()	

    # 0.N
    def mostrar_resultados_update(self):
        list_.append('Inicio de la función # 0.N << mostrar_resultados_update >>')        
        aux = ''
        i = 1
        for li in list_:
            print(li)
            aux =  aux + '<p>' + str(i) + ': ' + li + '</p>'
            i = i + 1
        self.resultados_update = aux
        list_.append('Salió de la función << mostrar_resultados_update >>')
        
        list_.clear()

    #- MENÚ PRINCIPAL PARA SINCRONIZAR ------------------------------------------------------------------------------------------------
    def main_down(self):
        # self.name = self.get_fecha_hora()
        
        # self.action_bajar_usuarios()
        credenciales = self.cargar_credenciales_bajada()
        if credenciales:
            self.reenmplazar_password()
            # self.action_actualizar_claves_usuarios()
            self.submenu_apoyo()
            self.sincronizar_transacciones(1)
        # self.reenmplazar_password()
        # self.actualizar_transaccion_sincronizada()
        # self.action_actualizar_claves_usuarios()
        self.mostrar_resultados_update()
        
        self.name_fin = self.get_fecha_hora()
        self.tiempo_transcurrido = str(self.restar_hora(self.name_fin,self.name))
        self.estatus = '2'
    
    def main_up(self):
        self.name = self.get_fecha_hora()
        
        # self.action_bajar_usuarios()
        credenciales = self.cargar_credenciales_subida()
        if credenciales:
            self.reenmplazar_password_up()
            # self.action_actualizar_claves_usuarios()
            # self.submenu_apoyo()
            self.sincronizar_transacciones(2)
        # self.reenmplazar_password()
        # self.actualizar_transaccion_sincronizada()
        # self.action_actualizar_claves_usuarios()
        self.mostrar_resultados_update()
        
        self.name_fin = self.get_fecha_hora()
        self.tiempo_transcurrido = str(self.restar_hora(self.name_fin,self.name))
        self.estatus = '2'
    
    estatus = fields.Selection([('0', 'Inicio'),
                                ('1', 'Proceso...'),
                                ('2', 'Finalizado')],
        string='Estatus', 
        default='0'
    )

    name = fields.Char(
        string='Fecha de inicio Sincronización de las Bases de Datos'
    )
    
    name_fin = fields.Char(
        string='Fecha fin de Sincronización de las Bases de Datos'
    )
    
    tiempo_transcurrido = fields.Char(
        string='Tiempo transcurrido'
    )
    
    resultados_update = fields.Html(string='Resultados de la Sincronización')

