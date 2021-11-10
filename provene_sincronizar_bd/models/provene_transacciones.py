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
    
    # @api.model
    # def create(self, values):
    #     user ={}
    #     numero = str(values['values_transaccion']['cedula'])
    #     if not self.env['provene.transaccion.bd'].search([('modelo_transaccion','=','registro.asesoria'),('values_transaccion','like',numero)],limit=1):
    #         # _logger.info('entre en create RegistroAsesoriaLegal********************************************************* 100000 \t\t\t\t %s \t\t\t\t ' % (res))
    #         user = super(TransaccionLaNave, self).create(values)
    #     return user


    
    def _fecha_hora_creacion(self):
        try:
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)  
            context_today = pytz.utc.localize(fields.Datetime.now()).astimezone(user_tz)
            return context_today.strftime("%d/%m/%Y %H:%M:%S")
            _logger.info('........................................................................... 1003 %s' % ( fields.Date.context_today(self).strftime("%d/%m/%Y %H:%M:%S")))
        except:
            return 0
            _logger.info('........................................................................... 3 %s' % ('Error al intentar colocar la fecha de Sincronización'))
    
    # 0.0 -A
    def action_bajar_usuarios(self):
        
        NOMBRE_TABLA = 'public.res_users'
        # NOMBRE_TABLA_REAL = 'public.registro_asesoria_registro_cuestionario1_c21_rel'
        NOMBRE_FUNCION = 'action_bajar_usuarios'
        list_.append('Inicio de la función # 0.0 - A << %s >>' % (NOMBRE_FUNCION))

        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        USER_LOCAL="openpg"
        PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
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
                                T2.tripulante_otros, 
                                T2.aceptar_manifiesto
                        FROM    dblink(	'host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 
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
    						dblink(	'host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 
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
                                            RU.chatter_position, 
                                            RU.telefono, 
                                            RU.tipo_tripulante, 
                                            RU.tripulante_otros, 
                                            RU.aceptar_manifiesto
                                            FROM res_users RU, res_partner RP, res_groups_users_rel RGU, res_groups RG
                                            WHERE 	RU.partner_id = RP.ID
						AND RG.ID = RGU.gid
						AND RU.ID = RGU.uid
						AND (RG.name like ''%Ajustes%'' OR RG.name like ''%Capitán%'')
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
                                                                    chatter_position varchar, 
                                                                    telefono varchar, 
                                                                    tipo_tripulante varchar, 
                                                                    tripulante_otros varchar, 
                                                                    aceptar_manifiesto varchar )
                        ON T1.login = T2.login
                        WHERE T1.login IS NULL 
                                """ 
            cur.execute(sql)
            if cur.rowcount > 0:
                usuarios = cur.fetchall()
                for usuario in usuarios:
                    if usuario[0] == 15:
                        permiso_acceso = True
                        creacion_contactos = True
                        capitan_tripulante = 'in_group_' + str((self.env['res.groups'].search([('name','like','%Capitán%')],limit=1)).id)
                        list_.append('capitan_tripulante........................................................................... 20 \t\t\t\t %s \t\t\t\t ' % (capitan_tripulante))
                        _logger.info('capitan_tripulante........................................................................... 20 \t\t\t\t %s \t\t\t\t ' % (capitan_tripulante))
                    else:
                        permiso_acceso = False
                        capitan_tripulante = 'in_group_' + str((self.env['res.groups'].search([('name','like','%Tripulante%')],limit=1)).id)
                        list_.append('capitan_tripulante........................................................................... 30 \t\t\t\t %s \t\t\t\t ' % (capitan_tripulante))
                        _logger.info('capitan_tripulante........................................................................... 30 \t\t\t\t %s \t\t\t\t ' % (capitan_tripulante))
                        creacion_contactos = False

                    values = {
                        'name': usuario[2],
                        'telefono': usuario[19],
                        'tipo_tripulante': usuario[20],
                        'login': usuario[5],
                        'lang': usuario[3],
                        'write_date': usuario[14],
                        'sel_groups_1_8_9':1,
                        'in_group_2':permiso_acceso,
                        capitan_tripulante:True,
                        'in_group_7':creacion_contactos
                    }
                    list_.append('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t %s' % (values, cur.statusmessage))
                    _logger.info('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t %s' % (values, cur.statusmessage))

                    record = self.env['res.users'].create(values)
                    list_.append('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t' % (record))
                    
                    _logger.info('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t ' % (record))
                list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
                self.action_actualizar_claves_usuarios()
            else:
                list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            # _logger.info('Casos Legales........................................................................... 1 %s' % (cur.statusmessage))
            self.mostrar_resultados_update()
                
        except (Exception, psycopg2.DatabaseError) as error:
            list_.append('Error: (%s). Al intentar insertar en la tabla << %s >> en la función action_bajar_casos_legal' %(error, NOMBRE_TABLA))
            _logger.info('Que carajo hace esto con los values........................................................................... 3 %s' % (error))
        finally:
            cur.close()
            conexion.close()  		

    # 0.0 - B
    def action_actualizar_claves_usuarios(self):
        NOMBRE_TABLA = 'public.res_users'
        # NOMBRE_TABLA_REAL = 'public.registro_asesoria_registro_cuestionario1_c21_rel'
        NOMBRE_FUNCION = 'action_actualizar_claves_usuarios'
        list_.append('Inicio de la función # 0.0 << %s >>' % (NOMBRE_FUNCION))

        try:
            # conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
            # cur = conexion.cursor()
            cur = self.env.cr
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
                                tripulante_otros, 
                                aceptar_manifiesto
                        FROM 	dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 
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
                                                chatter_position, 
                                                telefono, 
                                                tipo_tripulante, 
                                                tripulante_otros, 
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
                                            chatter_position varchar, 
                                            telefono varchar, 
                                            tipo_tripulante varchar, 
                                            tripulante_otros varchar, 
                                            aceptar_manifiesto varchar)
                                """
            cur.execute(sql)
            if cur.rowcount > 0:
                list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %(NOMBRE_TABLA))
                
                campo_actualizar = cur.fetchall()
                descripcion = cur.description
                for update_casos_legal in campo_actualizar:
                    i = 0
                    sql = """ 	SELECT 
								dblink_exec('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 
							"""	
                    sql = sql + '\' UPDATE  res_users SET '
                    for cd in descripcion:
                        if i == 3:
                            # Unicamente Actualiza la Clave de Usuario
                            sql = sql + cd.name + '=\'\'%s\'\'' % (update_casos_legal[i])
                        i=i+1
                    sql = sql + ' WHERE login=\'\'%s\'\' \' )' % (update_casos_legal[2])
                    cur.execute(sql)
                    # list_.append('Comentar Línea, SQL que construyó para modificar la tabla %s: \n %s \n' %(NOMBRE_TABLA, sql))
                    # list_.append('Registros que coinciden ---------------------->>>>>>>>>>>>>>>%s \n' %(cur.rowcount))
                    if cur.rowcount > 0:
                        # conexion.commit()
                        list_.append('Se actualizó el registro [login: %s] de la tabla << %s >> en la PC local (%s)' %(update_casos_legal[2],NOMBRE_TABLA,cur.statusmessage))
                        _logger.info('........................................................................... 1 %s TABLA %s en la funcion: %s' % (cur.statusmessage,NOMBRE_TABLA, NOMBRE_FUNCION))
                    else:
                        _logger.info('........................................................................... 2 %s TABLA %s en la funcion: %s' % (cur.statusmessage,NOMBRE_TABLA, NOMBRE_FUNCION))
                        list_.append('No hubo actualización en la tabla << %s >> de la PC local  para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                list_.append('------------------------------------------------------------------------------------------------------------')
                    # print(cur.statusmessage)
            else:
                _logger.info('........................................................................... 2 %s' % (cur.statusmessage))
                list_.append('La consulta NO encontró diferencias entre la tabla << %s >> del Servidor y la PC local (%s)' %(NOMBRE_TABLA,cur.statusmessage))			
                
        except (Exception, psycopg2.DatabaseError) as error:
            list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA,NOMBRE_FUNCION))
            _logger.info('........................................................................... 3 %s TABLA %s en la funcion: %s' % (error,NOMBRE_TABLA, NOMBRE_FUNCION))
        # finally:
            # cur.close()
            # conexion.close()     
    
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
    