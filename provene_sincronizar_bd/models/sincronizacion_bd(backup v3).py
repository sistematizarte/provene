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
import odoorpc
import ast


_logger = logging.getLogger(__name__)

list_ = []

class SincronizarBD(models.Model): 
    _name = 'provene.sincronizar.bd'
    
    ENTRAR_ACT_1 = True
    ENTRAR_ACT_2 = True
    
    # CREATE EXTENSION dblink para instalar la funcion dblink en base de datos
    
    @api.model
    def default_get(self,fields_list):
        res = super(SincronizarBD,self).default_get(fields_list)
        # res['nombre'] = fields.Date.today()
        try:
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)  
            context_today = pytz.utc.localize(fields.Datetime.now()).astimezone(user_tz)
            res.update({'name':context_today.strftime("%d/%m/%Y %H:%M:%S")})
            _logger.info('........................................................................... 1003 %s' % ( fields.Date.context_today(self).strftime("%d/%m/%Y %H:%M:%S")))
        except:
            _logger.info('........................................................................... 3 %s' % ('Error al intentar colocar la fecha de Sincronización'))
        return res
    
    def action_bajar_registro_asesoria(self):
    
        try:
            conexion = psycopg2.connect(host="127.0.0.1", database="provene_local_6", user="openpg", password="openpgpwd")       
            cur = conexion.cursor()
            cur.execute(""" INSERT INTO registro_asesoria 
                            (cedula , 
                            nombre  , 
                            apellido ,
                            fecha_nacimiento , 
                            direccion ,   
                            parroquia , 
                            municipio , 
                            estado , 
                            estado_civil ,  
                            genero , 
                            nacionalidad , 
                            estatus ,
                            datos_jornada_calendario    ,  
                            create_uid ,
                            create_date ,
                            write_uid , 
                            write_date ,
                            telefono_habitacion  ,   
                            telefono_celular  ,  
                            telefono_trabajo  ,     
                            hora_contacto ,
                            calle_callejon_av_trs ,   
                            escalera  , 
                            piso  , 
                            apartamento ,
                            barrio_urb_zona, 
                            casa_edif ,
                            foto_carnet_clave  
                            )
                        SELECT	T2.cedula , 
                                T2.nombre  , 
                                T2.apellido ,
                                T2.fecha_nacimiento , 
                                T2.direccion ,   
                                T2.parroquia , 
                                T2.municipio , 
                                T2.estado , 
                                T2.estado_civil ,  
                                T2.genero , 
                                T2.nacionalidad , 
                                T2.estatus ,
                                T2.datos_jornada_calendario    ,  
                                T2.create_uid ,
                                T2.create_date ,
                                T2.write_uid , 
                                T2.write_date ,
                                T2.telefono_habitacion  ,   
                                T2.telefono_celular  ,  
                                T2.telefono_trabajo  ,     
                                T2.hora_contacto ,
                                T2.calle_callejon_av_trs ,   
                                T2.escalera  , 
                                T2.piso  , 
                                T2.apartamento ,
                                T2.barrio_urb_zona, 
                                T2.casa_edif ,
                                T2.foto_carnet_clave  
                        FROM  dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 'SELECT  id,
                                                                                                                    cedula, 
                                                                                                                    nombre, 
                                                                                                                    apellido,
                                                                                                                    fecha_nacimiento, 
                                                                                                                    direccion, 
                                                                                                                    parroquia, 
                                                                                                                    municipio, 
                                                                                                                    estado, 
                                                                                                                    estado_civil,  
                                                                                                                    genero, 
                                                                                                                    nacionalidad , 
                                                                                                                    estatus,
                                                                                                                    datos_jornada_calendario    ,  
                                                                                                                    create_uid ,
                                                                                                                    create_date,
                                                                                                                    write_uid, 
                                                                                                                    write_date,
                                                                                                                    telefono_habitacion  ,   
                                                                                                                    telefono_celular  ,  
                                                                                                                    telefono_trabajo  ,     
                                                                                                                    hora_contacto,
                                                                                                                    calle_callejon_av_trs,    
                                                                                                                    escalera  , 
                                                                                                                    piso  , 
                                                                                                                    apartamento ,
                                                                                                                    barrio_urb_zona    , 
                                                                                                                        casa_edif,
                                                                                                                    foto_carnet_clave      

                                                                                                            FROM registro_asesoria')
                                                                    AS t1(  id integer,
                                                                        cedula varchar, 
                                                                        nombre varchar , 
                                                                        apellido varchar,
                                                                        fecha_nacimiento date, 
                                                                        direccion varchar,   
                                                                        parroquia integer, 
                                                                        municipio integer, 
                                                                        estado integer, 
                                                                        estado_civil varchar,  
                                                                        genero varchar, 
                                                                        nacionalidad integer, 
                                                                        estatus varchar,
                                                                        datos_jornada_calendario varchar   ,  
                                                                        create_uid integer,
                                                                        create_date timestamp,
                                                                        write_uid integer, 
                                                                        write_date timestamp,
                                                                        telefono_habitacion varchar ,   
                                                                        telefono_celular varchar ,  
                                                                        telefono_trabajo varchar ,     
                                                                        hora_contacto varchar,
                                                                        calle_callejon_av_trs varchar,   
                                                                        escalera varchar , 
                                                                        piso varchar , 
                                                                        apartamento varchar,
                                                                        barrio_urb_zona varchar   , 
                                                                        casa_edif varchar,
                                                                        foto_carnet_clave varchar )
                        RIGHT JOIN
                            dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 'SELECT  id,
                                                                                                                        cedula, 
                                                                                                                        nombre, 
                                                                                                                        apellido,
                                                                                                                        fecha_nacimiento, 
                                                                                                                        direccion, 
                                                                                                                        parroquia, 
                                                                                                                        municipio, 
                                                                                                                        estado, 
                                                                                                                        estado_civil,  
                                                                                                                        genero, 
                                                                                                                        nacionalidad , 
                                                                                                                        estatus,
                                                                                                                        datos_jornada_calendario    ,  
                                                                                                                        create_uid ,
                                                                                                                        create_date,
                                                                                                                        write_uid, 
                                                                                                                        write_date,
                                                                                                                        telefono_habitacion  ,   
                                                                                                                        telefono_celular  ,  
                                                                                                                        telefono_trabajo  ,     
                                                                                                                        hora_contacto,
                                                                                                                        calle_callejon_av_trs,    
                                                                                                                        escalera  , 
                                                                                                                        piso  , 
                                                                                                                        apartamento ,
                                                                                                                        barrio_urb_zona    , 
                                                                                                                        casa_edif,
                                                                                                                        foto_carnet_clave      

                                                                                                                    FROM registro_asesoria')
                                                                        AS t2(  id integer,
                                                                            cedula varchar, 
                                                                            nombre varchar , 
                                                                            apellido varchar,
                                                                            fecha_nacimiento date, 
                                                                            direccion varchar,   
                                                                            parroquia integer, 
                                                                            municipio integer, 
                                                                            estado integer, 
                                                                            estado_civil varchar,  
                                                                            genero varchar, 
                                                                            nacionalidad integer, 
                                                                            estatus varchar,
                                                                            datos_jornada_calendario varchar   ,  
                                                                            create_uid integer,
                                                                            create_date timestamp,
                                                                            write_uid integer, 
                                                                            write_date timestamp,
                                                                            telefono_habitacion varchar ,   
                                                                            telefono_celular varchar ,  
                                                                            telefono_trabajo varchar ,     
                                                                            hora_contacto varchar,
                                                                            calle_callejon_av_trs varchar,   
                                                                            escalera varchar , 
                                                                            piso varchar , 
                                                                            apartamento varchar,
                                                                            barrio_urb_zona varchar   , 
                                                                            casa_edif varchar,
                                                                            foto_carnet_clave varchar )
                        ON T1.cedula = T2.cedula
                        WHERE T1.CEDULA IS NULL 
                        """)
            conexion.commit()
            list_.append('Se actualizó la tabla <<  >> en la PC local (%s)' %(cur.statusmessage))
        except (Exception, psycopg2.DatabaseError) as error:
            # self.resultados_actualizar = str(error + '\n ' + self.resultados_actualizar)
            list_.append('Error en la tabla << registro_asesoria >> (%s)' %(error))
            _logger.info('Casos Legales action_bajar_registro_asesoria........................................................................... 3 %s' % (error))
                
        finally:
            conexion.close()   
    
    #1.1
    def action_bajar_registro_asesoria_y_create_uid(self):
        
        continuar_eje = True
        CONTINUAR_EJE_2 = True
        CONTINUAR_EJE_3 = 0
        NOMBRE_TABLA = 'public.registro_asesoria_aux'
        NOMBRE_TABLA_REAL = 'public.registro_asesoria'
        NOMBRE_FUNCION = 'action_bajar_registro_asesoria_y_create_uid'

        list_.append('Inicio de la función # 1.1 << %s >>' % (NOMBRE_FUNCION))

        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        USER_LOCAL="openpg"
        PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
            cur = conexion.cursor()
            sql = """ CREATE TABLE %s
                        (
                        id_ru integer NOT NULL,
                        login varchar,
                        id integer NOT NULL,
                        datos_jornada_calendario character varying NOT NULL, -- Nombre de la Jornada
                        nombre character varying NOT NULL, -- Nombres
                        apellido character varying NOT NULL, -- Apellidos
                        foto_carnet_clave text, -- Referencia Foto
                        nacionalidad_real character varying NOT NULL, -- Nacionalidad
                        cedula character varying(14) NOT NULL, -- Cédula
                        fecha_nacimiento date NOT NULL, -- Fecha de Nacimiento
                        email character varying, -- Correo Electrónico
                        genero character varying NOT NULL, -- Sexo
                        estado_civil character varying NOT NULL, -- Estado Civil
                        nacionalidad integer NOT NULL, -- Pais
                        estado integer NOT NULL, -- Estado
                        municipio integer NOT NULL, -- Municipio
                        parroquia integer NOT NULL, -- Parroquia
                        calle_callejon_av_trs character varying NOT NULL, -- Calle / Callejón / Av. / Trs.
                        casa_edif character varying NOT NULL, -- N° Casa / Edf.
                        escalera character varying, -- Escalera
                        piso character varying, -- Piso
                        apartamento character varying, -- Apartamento
                        barrio_urb_zona character varying NOT NULL, -- Barrio / Urb. / Zona
                        direccion text NOT NULL, -- Referencias
                        telefono_habitacion character varying(15), -- Teléfono de habitación
                        telefono_celular character varying(15), -- Teléfono Celular
                        telefono_trabajo character varying(15), -- Teléfono de Sitio de Trabajo
                        hora_contacto character varying, -- Hora posible de contacto
                        c4_nexo_familiar character varying, -- Nexo con el Jefe de Familia
                        c5_grado_instruccion character varying, -- Grado de Instrucción
                        c6_situacion_ocupacion character varying, -- Su Situación de Ocupación
                        c7_tipo_vivienda character varying, -- Tipo de Vivienda
                        c8_tenencia_vivienda character varying, -- Tenencia de Vivienda
                        c9_personas_viven_usted integer, -- Número de personas que viven con usted
                        c10_personas_menores_6 integer, -- ¿Cuántos son niños menores de 6 años?
                        c11_personas_menores_6_12 integer, -- ¿Cuántos son niños de 6 a 12 años?
                        c12_personas_menores_6_12_escuela character varying, -- ¿Esos niños de 6 a 12 años van a la escuela?
                        c13_frecuencia_escuela character varying, -- ¿Con qué frecuencia van los niños a la escuela?
                        c14_personas_ingresos integer, -- ¿Cuántas personas perciben algún ingreso en su hogar?
                        c15_ingreso_hogar character varying, -- ¿Es usted alguna de esas personas que reciben algún ingreso en su hogar?
                        c16_principal_hogar character varying, -- ¿Es usted el sustento principal del hogar?
                        c17_familia_exterior character varying, -- ¿Tiene usted o alguna otra persona de su hogar familiares directos en el exterior?
                        c18_ayuda_economica_exterior character varying, -- ¿Recibe usted  o alguna otra persona de su hogar ayuda económica desde el exterior?
                        c20_comidas_diarias character varying, -- ¿Hacen las tres comidas al día en su casa?
                        c22_referido character varying, -- Referido por:
                        cl1_servicio character varying, -- ¿Ha utilizado alguna vez algún servicio de PROVENE?
                        cl2_canalizar character varying, -- ¿Ha tenido alguna vez algún caso legal que no haya podido canalizar?
                        cl3_solicitar character varying, -- ¿Está aquí para solicitar algún trámite legal o asistencia jurídica?
                        cl4_asistencia character varying, -- ¿Es la primera vez que busca este tipo de asistencia?
                        cl5_tramite character varying, -- ¿Qué tipo de trámite necesitaría?
                        cl6_tribunales character varying, -- ¿Ha ido usted previamente a los tribunales a resolver asuntos legales?
                        cl7_experiencia character varying, -- ¿Cómo ha sido tu experiencia?
                        cl8_ddhh character varying, -- ¿Considera usted que en Venezuela se violan los DDHH?
                        cl9_justicia character varying, -- ¿Considera usted que en Venezuela hay justicia?
                        cl10_transicional character varying, -- ¿Sabe usted qué es la Justicia Transicional?
                        cs1_actividad character varying, -- ¿Ha participado usted en alguna actividad o taller de carácter social, tal como Taller de arte, Cine foro, Danza, Teatro social, Música o de algún otro tipo?
                        cs3_capacidad character varying, -- ¿Se siente usted en la capacidad de mejorar su vida y la de su familia?
                        cs5_contribuir character varying, -- ¿Le gustaría a usted, estaría dispuesto a contribuir con su comunidad, mejorar su comunidad?
                        cs7_participar_actividades character varying, -- ¿Le gustaría a usted, estaría  dispuesto a participar en las actividades sociales que propone La Nave?
                        cs8_ayuda_economica_exterior text, -- ¿Por qué no sabes o no estarías dispuesto a participar en La Nave?
                        create_uid integer, -- Created by
                        create_date timestamp without time zone, -- Created on
                        write_uid integer, -- Last Updated by
                        write_date timestamp without time zone, -- Last Updated on
                        )
                """ % (NOMBRE_TABLA)
            cur.execute(sql)
            continuar_eje = True
            list_.append('Se creó la tabla temporal << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            _logger.info('........................................................................................................1 %s' % (cur.statusmessage))    
                
        except (Exception, psycopg2.DatabaseError) as error:
            if error.pgcode != '42P07':
                continuar_eje = False
                list_.append('Error: %s. Al intentar crear la tabla temporal << %s >> con la función %s' % (error, NOMBRE_TABLA, NOMBRE_FUNCION))
                _logger.info('....................................................................................................3 %s' % (error))

        if continuar_eje:

            try:
                sql = 'DELETE FROM %s ' % (NOMBRE_TABLA)
                cur.execute(sql)
                list_.append('Se limpió la información de la tabla temporal << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                _logger.info('....................................................................................................1 %s' % (cur.statusmessage))
            except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar limpiar la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA , NOMBRE_FUNCION))
                _logger.info('....................................................................................................3 %s' % (error))
            try:
                sql = """ 	INSERT INTO %s 
                                    (id_ru,
                                        login,
                                        id,
                                        datos_jornada_calendario,
                                        nombre,
                                        apellido,
                                        foto_carnet_clave,
                                        nacionalidad_real,
                                        cedula,
                                        fecha_nacimiento,
                                        email,
                                        genero,
                                        estado_civil,
                                        nacionalidad ,
                                        estado ,
                                        municipio ,
                                        parroquia ,
                                        calle_callejon_av_trs,
                                        casa_edif,
                                        escalera,
                                        piso,
                                        apartamento,
                                        barrio_urb_zona,
                                        direccion,
                                        telefono_habitacion,
                                        telefono_celular,
                                        telefono_trabajo,
                                        hora_contacto,
                                        c4_nexo_familiar,
                                        c5_grado_instruccion,
                                        c6_situacion_ocupacion,
                                        c7_tipo_vivienda,
                                        c8_tenencia_vivienda,
                                        c9_personas_viven_usted ,
                                        c10_personas_menores_6 ,
                                        c11_personas_menores_6_12 ,
                                        c12_personas_menores_6_12_escuela,
                                        c13_frecuencia_escuela,
                                        c14_personas_ingresos ,
                                        c15_ingreso_hogar,
                                        c16_principal_hogar,
                                        c17_familia_exterior,
                                        c18_ayuda_economica_exterior,
                                        c20_comidas_diarias,
                                        c22_referido,
                                        cl1_servicio,
                                        cl2_canalizar,
                                        cl3_solicitar,
                                        cl4_asistencia,
                                        cl5_tramite,
                                        cl6_tribunales,
                                        cl7_experiencia,
                                        cl8_ddhh,
                                        cl9_justicia,
                                        cl10_transicional,
                                        cs1_actividad,
                                        cs3_capacidad,
                                        cs5_contribuir,
                                        cs7_participar_actividades,
                                        cs8_ayuda_economica_exterior,
                                        create_uid ,
                                        create_date ,
                                        write_uid ,
                                        write_date )
                                        SELECT RU.id, 
																		T3.login,
																		T3.id ,
												T3.datos_jornada_calendario,
												T3.nombre,
												T3.apellido,
												T3.foto_carnet_clave,
												T3.nacionalidad_real,
												T3.cedula,
												T3.fecha_nacimiento,
												T3.email,
												T3.genero,
												T3.estado_civil,
												T3.nacionalidad ,
												T3.estado ,
												T3.municipio ,
												T3.parroquia ,
												T3.calle_callejon_av_trs,
												T3.casa_edif,
												T3.escalera,
												T3.piso,
												T3.apartamento,
												T3.barrio_urb_zona,
												T3.direccion,
												T3.telefono_habitacion,
												T3.telefono_celular,
												T3.telefono_trabajo,
												T3.hora_contacto,
												T3.c4_nexo_familiar,
												T3.c5_grado_instruccion,
												T3.c6_situacion_ocupacion,
												T3.c7_tipo_vivienda,
												T3.c8_tenencia_vivienda,
												T3.c9_personas_viven_usted ,
												T3.c10_personas_menores_6 ,
												T3.c11_personas_menores_6_12 ,
												T3.c12_personas_menores_6_12_escuela,
												T3.c13_frecuencia_escuela,
												T3.c14_personas_ingresos ,
												T3.c15_ingreso_hogar,
												T3.c16_principal_hogar,
												T3.c17_familia_exterior,
												T3.c18_ayuda_economica_exterior,
												T3.c20_comidas_diarias,
												T3.c22_referido,
												T3.cl1_servicio,
												T3.cl2_canalizar,
												T3.cl3_solicitar,
												T3.cl4_asistencia,
												T3.cl5_tramite,
												T3.cl6_tribunales,
												T3.cl7_experiencia,
												T3.cl8_ddhh,
												T3.cl9_justicia,
												T3.cl10_transicional,
												T3.cs1_actividad,
												T3.cs3_capacidad,
												T3.cs5_contribuir,
												T3.cs7_participar_actividades,
												T3.cs8_ayuda_economica_exterior,
												T3.create_uid ,
												T3.create_date ,
												T3.write_uid ,
												T3.write_date 
																		FROM (
																		SELECT	T2.login,
																		T2.id ,
								T2.datos_jornada_calendario,
								T2.nombre,
								T2.apellido,
								T2.foto_carnet_clave,
								T2.nacionalidad_real,
								T2.cedula,
								T2.fecha_nacimiento,
								T2.email,
								T2.genero,
								T2.estado_civil,
								T2.nacionalidad ,
								T2.estado ,
								T2.municipio ,
								T2.parroquia ,
								T2.calle_callejon_av_trs,
								T2.casa_edif,
								T2.escalera,
								T2.piso,
								T2.apartamento,
								T2.barrio_urb_zona,
								T2.direccion,
								T2.telefono_habitacion,
								T2.telefono_celular,
								T2.telefono_trabajo,
								T2.hora_contacto,
								T2.c4_nexo_familiar,
								T2.c5_grado_instruccion,
								T2.c6_situacion_ocupacion,
								T2.c7_tipo_vivienda,
								T2.c8_tenencia_vivienda,
								T2.c9_personas_viven_usted ,
								T2.c10_personas_menores_6 ,
								T2.c11_personas_menores_6_12 ,
								T2.c12_personas_menores_6_12_escuela,
								T2.c13_frecuencia_escuela,
								T2.c14_personas_ingresos ,
								T2.c15_ingreso_hogar,
								T2.c16_principal_hogar,
								T2.c17_familia_exterior,
								T2.c18_ayuda_economica_exterior,
								T2.c20_comidas_diarias,
								T2.c22_referido,
								T2.cl1_servicio,
								T2.cl2_canalizar,
								T2.cl3_solicitar,
								T2.cl4_asistencia,
								T2.cl5_tramite,
								T2.cl6_tribunales,
								T2.cl7_experiencia,
								T2.cl8_ddhh,
								T2.cl9_justicia,
								T2.cl10_transicional,
								T2.cs1_actividad,
								T2.cs3_capacidad,
								T2.cs5_contribuir,
								T2.cs7_participar_actividades,
								T2.cs8_ayuda_economica_exterior,
								T2.create_uid ,
								T2.create_date ,
								T2.write_uid ,
								T2.write_date 
															FROM  dblink(   'host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 
																														'SELECT id ,
								datos_jornada_calendario,
								nombre,
								apellido,
								foto_carnet_clave,
								nacionalidad_real,
								cedula,
								fecha_nacimiento,
								email,
								genero,
								estado_civil,
								nacionalidad ,
								estado ,
								municipio ,
								parroquia ,
								calle_callejon_av_trs,
								casa_edif,
								escalera,
								piso,
								apartamento,
								barrio_urb_zona,
								direccion,
								telefono_habitacion,
								telefono_celular,
								telefono_trabajo,
								hora_contacto,
								c4_nexo_familiar,
								c5_grado_instruccion,
								c6_situacion_ocupacion,
								c7_tipo_vivienda,
								c8_tenencia_vivienda,
								c9_personas_viven_usted ,
								c10_personas_menores_6 ,
								c11_personas_menores_6_12 ,
								c12_personas_menores_6_12_escuela,
								c13_frecuencia_escuela,
								c14_personas_ingresos ,
								c15_ingreso_hogar,
								c16_principal_hogar,
								c17_familia_exterior,
								c18_ayuda_economica_exterior,
								c20_comidas_diarias,
								c22_referido,
								cl1_servicio,
								cl2_canalizar,
								cl3_solicitar,
								cl4_asistencia,
								cl5_tramite,
								cl6_tribunales,
								cl7_experiencia,
								cl8_ddhh,
								cl9_justicia,
								cl10_transicional,
								cs1_actividad,
								cs3_capacidad,
								cs5_contribuir,
								cs7_participar_actividades,
								cs8_ayuda_economica_exterior,
								create_uid ,
								create_date ,
								write_uid ,
								write_date 
																																FROM registro_asesoria')  AS t1(id integer,
								datos_jornada_calendario character varying,
								nombre character varying,
								apellido character varying,
								foto_carnet_clave text,
								nacionalidad_real character varying,
								cedula character varying,
								fecha_nacimiento date,
								email character varying,
								genero character varying,
								estado_civil character varying,
								nacionalidad integer,
								estado integer,
								municipio integer,
								parroquia integer,
								calle_callejon_av_trs character varying,
								casa_edif character varying,
								escalera character varying,
								piso character varying,
								apartamento character varying,
								barrio_urb_zona character varying,
								direccion text,
								telefono_habitacion character varying,
								telefono_celular character varying,
								telefono_trabajo character varying,
								hora_contacto character varying,
								c4_nexo_familiar character varying,
								c5_grado_instruccion character varying,
								c6_situacion_ocupacion character varying,
								c7_tipo_vivienda character varying,
								c8_tenencia_vivienda character varying,
								c9_personas_viven_usted integer,
								c10_personas_menores_6 integer,
								c11_personas_menores_6_12 integer,
								c12_personas_menores_6_12_escuela character varying,
								c13_frecuencia_escuela character varying,
								c14_personas_ingresos integer,
								c15_ingreso_hogar character varying,
								c16_principal_hogar character varying,
								c17_familia_exterior character varying,
								c18_ayuda_economica_exterior character varying,
								c20_comidas_diarias character varying,
								c22_referido character varying,
								cl1_servicio character varying,
								cl2_canalizar character varying,
								cl3_solicitar character varying,
								cl4_asistencia character varying,
								cl5_tramite character varying,
								cl6_tribunales character varying,
								cl7_experiencia character varying,
								cl8_ddhh character varying,
								cl9_justicia character varying,
								cl10_transicional character varying,
								cs1_actividad character varying,
								cs3_capacidad character varying,
								cs5_contribuir character varying,
								cs7_participar_actividades character varying,
								cs8_ayuda_economica_exterior text,
								create_uid integer,
								create_date timestamp,
								write_uid integer,
								write_date timestamp )
																								RIGHT JOIN 
									dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 
																														'SELECT   RU.login, 
																										CL.id  ,
								datos_jornada_calendario,
								nombre,
								apellido,
								foto_carnet_clave,
								nacionalidad_real,
								cedula,
								fecha_nacimiento,
								email,
								genero,
								estado_civil,
								nacionalidad ,
								estado ,
								municipio ,
								parroquia ,
								calle_callejon_av_trs,
								casa_edif,
								escalera,
								piso,
								apartamento,
								barrio_urb_zona,
								direccion,
								telefono_habitacion,
								telefono_celular,
								telefono_trabajo,
								hora_contacto,
								c4_nexo_familiar,
								c5_grado_instruccion,
								c6_situacion_ocupacion,
								c7_tipo_vivienda,
								c8_tenencia_vivienda,
								c9_personas_viven_usted ,
								c10_personas_menores_6 ,
								c11_personas_menores_6_12 ,
								c12_personas_menores_6_12_escuela,
								c13_frecuencia_escuela,
								c14_personas_ingresos ,
								c15_ingreso_hogar,
								c16_principal_hogar,
								c17_familia_exterior,
								c18_ayuda_economica_exterior,
								c20_comidas_diarias,
								c22_referido,
								cl1_servicio,
								cl2_canalizar,
								cl3_solicitar,
								cl4_asistencia,
								cl5_tramite,
								cl6_tribunales,
								cl7_experiencia,
								cl8_ddhh,
								cl9_justicia,
								cl10_transicional,
								cs1_actividad,
								cs3_capacidad,
								cs5_contribuir,
								cs7_participar_actividades,
								cs8_ayuda_economica_exterior,
                                                                                                    CL.create_uid , 
                                                                                                    CL.create_date, 
                                                                                                    CL.write_uid , 
                                                                                                    CL.write_date    
                                                                                            FROM registro_asesoria CL, res_users RU
                                                                                            WHERE CL.create_uid = RU.id')  AS t2(login character varying,
											id integer,
											datos_jornada_calendario character varying,
											nombre character varying,
											apellido character varying,
											foto_carnet_clave text,
											nacionalidad_real character varying,
											cedula character varying,
											fecha_nacimiento date,
											email character varying,
											genero character varying,
											estado_civil character varying,
											nacionalidad integer,
											estado integer,
											municipio integer,
											parroquia integer,
											calle_callejon_av_trs character varying,
											casa_edif character varying,
											escalera character varying,
											piso character varying,
											apartamento character varying,
											barrio_urb_zona character varying,
											direccion text,
											telefono_habitacion character varying,
											telefono_celular character varying,
											telefono_trabajo character varying,
											hora_contacto character varying,
											c4_nexo_familiar character varying,
											c5_grado_instruccion character varying,
											c6_situacion_ocupacion character varying,
											c7_tipo_vivienda character varying,
											c8_tenencia_vivienda character varying,
											c9_personas_viven_usted integer,
											c10_personas_menores_6 integer,
											c11_personas_menores_6_12 integer,
											c12_personas_menores_6_12_escuela character varying,
											c13_frecuencia_escuela character varying,
											c14_personas_ingresos integer,
											c15_ingreso_hogar character varying,
											c16_principal_hogar character varying,
											c17_familia_exterior character varying,
											c18_ayuda_economica_exterior character varying,
											c20_comidas_diarias character varying,
											c22_referido character varying,
											cl1_servicio character varying,
											cl2_canalizar character varying,
											cl3_solicitar character varying,
											cl4_asistencia character varying,
											cl5_tramite character varying,
											cl6_tribunales character varying,
											cl7_experiencia character varying,
											cl8_ddhh character varying,
											cl9_justicia character varying,
											cl10_transicional character varying,
											cs1_actividad character varying,
											cs3_capacidad character varying,
											cs5_contribuir character varying,
											cs7_participar_actividades character varying,
											cs8_ayuda_economica_exterior text,
											create_uid integer,
											create_date timestamp,
											write_uid integer,
											write_date timestamp )
																								ON T1.create_date = T2.create_date
                                                    WHERE T1.create_date IS NULL) T3, res_users RU
                            WHERE T3.LOGIN = RU.LOGIN
                    """ % (NOMBRE_TABLA)
                cur.execute(sql)
                if cur.rowcount > 0:
                    list_.append('Se insertó en la tabla temporal << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
                    CONTINUAR_EJE_2 = True
                else:
                    list_.append('No hubo inserciones en la tabla temporal << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                    CONTINUAR_EJE_2 = False
            except (Exception, psycopg2.DatabaseError) as error:
                    list_.append('Error: %s. Al intentar insertar registros la tabla temporal << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                    _logger.info('....................................................................................................3 %s' % (error))
                    CONTINUAR_EJE_2 = False

            if CONTINUAR_EJE_2:
                # Actualizan los campos cuando en el Servidor hay un cambio, en caso contrario esta consulta es vacia
                try:
                    sql = 	"""	SELECT *
                                FROM %s
                            """ % (NOMBRE_TABLA)
                    cur.execute(sql)
                    if cur.rowcount > 0:
                        list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %('registro_asesoria'))
                        campo_actualizar = cur.fetchall()
                        descripcion = cur.description
                        CONTINUAR_EJE_3 = 0
                        
                        for update_casos_legal in campo_actualizar:
                            sql = ' UPDATE  %s SET ' % (NOMBRE_TABLA)
                            sql = sql + 'create_uid=\'%s\', create_date=\'%s\', write_date=\'%s\'' % (update_casos_legal[0],
                                                                                                        update_casos_legal[61],
                                                                                                        update_casos_legal[63])
                            
                            sql = sql + ' WHERE cedula=\'%s\' AND datos_jornada_calendario=\'%s\' '  % (update_casos_legal[8],
                                                                                                        update_casos_legal[3])
                            cur.execute(sql)
                            
                            if cur.rowcount > 0:
                                CONTINUAR_EJE_3 = CONTINUAR_EJE_3 + 1
                                list_.append('Se actualizó el registro [CI: %s Nom.: %s] de la tabla << %s >> en la PC local (%s)' %(update_casos_legal[8],update_casos_legal[4],NOMBRE_TABLA,cur.statusmessage))
                            else:
                                list_.append('No hubo actualización en la tabla << %s >> de la PC local  para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                        list_.append('------------------------------------------------------------------------------------------------------------')
                    else:
                        list_.append('La consulta NO encontró diferencias entre la tabla << %s >> del Servidor y la PC local (%s)' %('registro_asesoria',cur.statusmessage))			
                        print(cur.statusmessage)
                except (Exception, psycopg2.DatabaseError) as error:
                        list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                        _logger.info('....................................................................................................3 %s' % (error))
                    
                if CONTINUAR_EJE_3 > 0:
                    
                    try:
                        
                        sql = 'ALTER TABLE %s DISABLE TRIGGER ALL' %(NOMBRE_TABLA_REAL)
                        cur.execute(sql)
                        list_.append('Se deshabilitaron los TRIGGER de la tabla << %s >> (%s)' %(NOMBRE_TABLA_REAL,cur.statusmessage))
                        
                        sql = """ 	INSERT INTO %s 
                                        (datos_jornada_calendario,
                                            nombre,
                                            apellido,
                                            foto_carnet_clave,
                                            nacionalidad_real,
                                            cedula,
                                            fecha_nacimiento,
                                            email,
                                            genero,
                                            estado_civil,
                                            nacionalidad ,
                                            estado ,
                                            municipio ,
                                            parroquia ,
                                            calle_callejon_av_trs,
                                            casa_edif,
                                            escalera,
                                            piso,
                                            apartamento,
                                            barrio_urb_zona,
                                            direccion,
                                            telefono_habitacion,
                                            telefono_celular,
                                            telefono_trabajo,
                                            hora_contacto,
                                            c4_nexo_familiar,
                                            c5_grado_instruccion,
                                            c6_situacion_ocupacion,
                                            c7_tipo_vivienda,
                                            c8_tenencia_vivienda,
                                            c9_personas_viven_usted ,
                                            c10_personas_menores_6 ,
                                            c11_personas_menores_6_12 ,
                                            c12_personas_menores_6_12_escuela,
                                            c13_frecuencia_escuela,
                                            c14_personas_ingresos ,
                                            c15_ingreso_hogar,
                                            c16_principal_hogar,
                                            c17_familia_exterior,
                                            c18_ayuda_economica_exterior,
                                            c20_comidas_diarias,
                                            c22_referido,
                                            cl1_servicio,
                                            cl2_canalizar,
                                            cl3_solicitar,
                                            cl4_asistencia,
                                            cl5_tramite,
                                            cl6_tribunales,
                                            cl7_experiencia,
                                            cl8_ddhh,
                                            cl9_justicia,
                                            cl10_transicional,
                                            cs1_actividad,
                                            cs3_capacidad,
                                            cs5_contribuir,
                                            cs7_participar_actividades,
                                            cs8_ayuda_economica_exterior,
                                            create_uid ,
                                            create_date ,
                                            write_uid ,
                                            write_date )
                                    SELECT 	T3.datos_jornada_calendario,
												T3.nombre,
												T3.apellido,
												T3.foto_carnet_clave,
												T3.nacionalidad_real,
												T3.cedula,
												T3.fecha_nacimiento,
												T3.email,
												T3.genero,
												T3.estado_civil,
												T3.nacionalidad ,
												T3.estado ,
												T3.municipio ,
												T3.parroquia ,
												T3.calle_callejon_av_trs,
												T3.casa_edif,
												T3.escalera,
												T3.piso,
												T3.apartamento,
												T3.barrio_urb_zona,
												T3.direccion,
												T3.telefono_habitacion,
												T3.telefono_celular,
												T3.telefono_trabajo,
												T3.hora_contacto,
												T3.c4_nexo_familiar,
												T3.c5_grado_instruccion,
												T3.c6_situacion_ocupacion,
												T3.c7_tipo_vivienda,
												T3.c8_tenencia_vivienda,
												T3.c9_personas_viven_usted ,
												T3.c10_personas_menores_6 ,
												T3.c11_personas_menores_6_12 ,
												T3.c12_personas_menores_6_12_escuela,
												T3.c13_frecuencia_escuela,
												T3.c14_personas_ingresos ,
												T3.c15_ingreso_hogar,
												T3.c16_principal_hogar,
												T3.c17_familia_exterior,
												T3.c18_ayuda_economica_exterior,
												T3.c20_comidas_diarias,
												T3.c22_referido,
												T3.cl1_servicio,
												T3.cl2_canalizar,
												T3.cl3_solicitar,
												T3.cl4_asistencia,
												T3.cl5_tramite,
												T3.cl6_tribunales,
												T3.cl7_experiencia,
												T3.cl8_ddhh,
												T3.cl9_justicia,
												T3.cl10_transicional,
												T3.cs1_actividad,
												T3.cs3_capacidad,
												T3.cs5_contribuir,
												T3.cs7_participar_actividades,
												T3.cs8_ayuda_economica_exterior,
												T3.create_uid ,
												T3.create_date ,
												T3.write_uid ,
												T3.write_date 
                                    FROM 	%s T3""" % (NOMBRE_TABLA_REAL , NOMBRE_TABLA)
                        cur.execute(sql)
                        if cur.rowcount > 0:
                            list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA_REAL,cur.statusmessage))
                        else:
                            list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA_REAL,cur.statusmessage))
                        print(cur.statusmessage)
                        
                        sql = 'ALTER TABLE %s ENABLE TRIGGER ALL' % (NOMBRE_TABLA_REAL)
                        cur.execute(sql)
                        list_.append('Se habilitaron los TRIGGER de la tabla << %s >> (%s)' %(NOMBRE_TABLA_REAL , cur.statusmessage))
                            
                    except (Exception, psycopg2.DatabaseError) as error:
                        print(error)
                        list_.append('Error: (%s). Al intentar insertar en la tabla << %s >> en la función action_bajar_casos_legal' %(error, 'registro_asesoria'))
                        _logger.info('Casos Legales ........................................................................... 3 %s' % (error))
                        self.ENTRAR_ACT_1 = False
                        list_.append('ENTRAR_ACT_1: %s' % (self.ENTRAR_ACT_1))
                else:
                    list_.append("No habían datos en <<%s>> que actualizar" % (NOMBRE_TABLA))
                    self.ENTRAR_ACT_1 = False
                    list_.append('ENTRAR_ACT_1: %s' % (self.ENTRAR_ACT_1))
            else:
                list_.append("No se puede continuar porque la TABLA << %s >> ¡ESTÁ VACÍA!" % (NOMBRE_TABLA))
                self.ENTRAR_ACT_1 = False
                list_.append('ENTRAR_ACT_1: %s' % (self.ENTRAR_ACT_1))
            try:
                sql = 'DROP TABLE %s ' % (NOMBRE_TABLA)
                cur.execute(sql)
                conexion.commit()
                # continuar_eje = True
                list_.append('Se Eliminó la tabla temporal << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                print(cur.statusmessage)   
                    
            except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar eliminar la tabla temporal << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                _logger.info('Casos Legales ........................................................................... 3 %s' % (error))
                self.ENTRAR_ACT_1 = False
                list_.append('ENTRAR_ACT_1: %s' % (self.ENTRAR_ACT_1))
            finally:
                cur.close()
                conexion.close()
        else:
            list_.append("No se pudo continuar ejecutando esta función porque la TABLA PIVOTE << %s >> generó un error " % (NOMBRE_TABLA))
            self.ENTRAR_ACT_1 = False
            list_.append('ENTRAR_ACT_1: %s' % (self.ENTRAR_ACT_1))
        
        self.mostrar_resultados_update()

    #1.2
    def action_actualizar_registro_asesoria_sin_campos_relacion(self):
        
        NOMBRE_TABLA = 'public.registro_asesoria'
        NOMBRE_FUNCION = 'action_actualizar_registro_asesoria_sin_campos_relacion'
        list_.append('Inicio de la función # 1.2 << %s >>' % (NOMBRE_FUNCION))

        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        USER_LOCAL="openpg"
        PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
            cur = conexion.cursor()
            
            sql = 'ALTER TABLE %s DISABLE TRIGGER ALL' %(NOMBRE_TABLA)
            cur.execute(sql)
            conexion.commit()
            list_.append('Se deshabilitaron los TRIGGER de la tabla << %s >> (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                        
            
            sql = """  	SELECT  T2.datos_jornada_calendario,
                                T2.estatus,
                                T2.nombre,
                                T2.apellido,
                                T2.foto_carnet_clave,
                                T2.cedula,
                                T2.fecha_nacimiento,
                                T2.edad_,
                                T2.email,
                                T2.genero,
                                T2.estado_civil,
                                T2.nacionalidad,
                                T2.estado,
                                T2.municipio,
                                T2.parroquia,
                                T2.calle_callejon_av_trs,
                                T2.casa_edif,
                                T2.escalera,
                                T2.piso,
                                T2.apartamento,
                                T2.barrio_urb_zona,
                                T2.direccion,
                                T2.telefono_habitacion,
                                T2.telefono_celular,
                                T2.telefono_trabajo,
                                T2.hora_contacto,
                                T2.c4_nexo_familiar,
                                T2.c5_grado_instruccion,
                                T2.c6_situacion_ocupacion,
                                T2.c7_tipo_vivienda,
                                T2.c8_tenencia_vivienda,
                                T2.c9_personas_viven_usted,
                                T2.c10_personas_menores_6,
                                T2.c11_personas_menores_6_12,
                                T2.c12_personas_menores_6_12_escuela,
                                T2.c13_frecuencia_escuela,
                                T2.c14_personas_ingresos,
                                T2.c15_ingreso_hogar,
                                T2.c16_principal_hogar,
                                T2.c17_familia_exterior,
                                T2.c18_ayuda_economica_exterior,
                                T2.c20_comidas_diarias,
                                T2.create_uid,
                                T2.create_date,
                                T2.write_uid,
                                T2.write_date
                        FROM  dblink(   'host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 
                                        'SELECT id,
                                                datos_jornada_calendario,
                                                estatus,
                                                nombre,
                                                apellido,
                                                foto_carnet_clave,
                                                cedula,
                                                fecha_nacimiento,
                                                edad_,
                                                email,
                                                genero,
                                                estado_civil,
                                                nacionalidad,
                                                estado,
                                                municipio,
                                                parroquia,
                                                calle_callejon_av_trs,
                                                casa_edif,
                                                escalera,
                                                piso,
                                                apartamento,
                                                barrio_urb_zona,
                                                direccion,
                                                telefono_habitacion,
                                                telefono_celular,
                                                telefono_trabajo,
                                                hora_contacto,
                                                c4_nexo_familiar,
                                                c5_grado_instruccion,
                                                c6_situacion_ocupacion,
                                                c7_tipo_vivienda,
                                                c8_tenencia_vivienda,
                                                c9_personas_viven_usted,
                                                c10_personas_menores_6,
                                                c11_personas_menores_6_12,
                                                c12_personas_menores_6_12_escuela,
                                                c13_frecuencia_escuela,
                                                c14_personas_ingresos,
                                                c15_ingreso_hogar,
                                                c16_principal_hogar,
                                                c17_familia_exterior,
                                                c18_ayuda_economica_exterior,
                                                c20_comidas_diarias,
                                                create_uid,
                                                create_date,
                                                write_uid,
                                                write_date  
                                                FROM registro_asesoria')  AS t1(id integer,
                                                                                datos_jornada_calendario character varying,
                                                                                estatus character varying,
                                                                                nombre character varying,
                                                                                apellido character varying,
                                                                                foto_carnet_clave text,
                                                                                cedula character varying,
                                                                                fecha_nacimiento date,
                                                                                edad_ integer,
                                                                                email character varying,
                                                                                genero character varying,
                                                                                estado_civil character varying,
                                                                                nacionalidad integer,
                                                                                estado integer,
                                                                                municipio integer,
                                                                                parroquia integer,
                                                                                calle_callejon_av_trs character varying,
                                                                                casa_edif character varying,
                                                                                escalera character varying,
                                                                                piso character varying,
                                                                                apartamento character varying,
                                                                                barrio_urb_zona character varying,
                                                                                direccion text,
                                                                                telefono_habitacion character varying,
                                                                                telefono_celular character varying,
                                                                                telefono_trabajo character varying,
                                                                                hora_contacto character varying,
                                                                                c4_nexo_familiar character varying,
                                                                                c5_grado_instruccion character varying,
                                                                                c6_situacion_ocupacion character varying,
                                                                                c7_tipo_vivienda character varying,
                                                                                c8_tenencia_vivienda character varying,
                                                                                c9_personas_viven_usted integer,
                                                                                c10_personas_menores_6 integer,
                                                                                c11_personas_menores_6_12 integer,
                                                                                c12_personas_menores_6_12_escuela character varying,
                                                                                c13_frecuencia_escuela character varying,
                                                                                c14_personas_ingresos integer,
                                                                                c15_ingreso_hogar character varying,
                                                                                c16_principal_hogar character varying,
                                                                                c17_familia_exterior character varying,
                                                                                c18_ayuda_economica_exterior character varying,
                                                                                c20_comidas_diarias character varying,
                                                                                create_uid integer,
                                                                                create_date timestamp,
                                                                                write_uid integer,
                                                                                write_date timestamp )
                        RIGHT JOIN dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 
                                        'SELECT     id  ,
                                                    datos_jornada_calendario,
                                                    estatus,
                                                    nombre,
                                                    apellido,
                                                    foto_carnet_clave,
                                                    cedula,
                                                    fecha_nacimiento,
                                                    edad_,
                                                    email,
                                                    genero,
                                                    estado_civil,
                                                    nacionalidad,
                                                    estado,
                                                    municipio,
                                                    parroquia,
                                                    calle_callejon_av_trs,
                                                    casa_edif,
                                                    escalera,
                                                    piso,
                                                    apartamento,
                                                    barrio_urb_zona,
                                                    direccion,
                                                    telefono_habitacion,
                                                    telefono_celular,
                                                    telefono_trabajo,
                                                    hora_contacto,
                                                    c4_nexo_familiar,
                                                    c5_grado_instruccion,
                                                    c6_situacion_ocupacion,
                                                    c7_tipo_vivienda,
                                                    c8_tenencia_vivienda,
                                                    c9_personas_viven_usted,
                                                    c10_personas_menores_6,
                                                    c11_personas_menores_6_12,
                                                    c12_personas_menores_6_12_escuela,
                                                    c13_frecuencia_escuela,
                                                    c14_personas_ingresos,
                                                    c15_ingreso_hogar,
                                                    c16_principal_hogar,
                                                    c17_familia_exterior,
                                                    c18_ayuda_economica_exterior,
                                                    c20_comidas_diarias,
                                                    create_uid , 
                                                    create_date, 
                                                    write_uid , 
                                                    write_date    
                                            FROM registro_asesoria')  AS t2(id integer,
                                                                            datos_jornada_calendario character varying,
                                                                            estatus character varying,
                                                                            nombre character varying,
                                                                            apellido character varying,
                                                                            foto_carnet_clave text,
                                                                            cedula character varying,
                                                                            fecha_nacimiento date,
                                                                            edad_ integer,
                                                                            email character varying,
                                                                            genero character varying,
                                                                            estado_civil character varying,
                                                                            nacionalidad integer,
                                                                            estado integer,
                                                                            municipio integer,
                                                                            parroquia integer,
                                                                            calle_callejon_av_trs character varying,
                                                                            casa_edif character varying,
                                                                            escalera character varying,
                                                                            piso character varying,
                                                                            apartamento character varying,
                                                                            barrio_urb_zona character varying,
                                                                            direccion text,
                                                                            telefono_habitacion character varying,
                                                                            telefono_celular character varying,
                                                                            telefono_trabajo character varying,
                                                                            hora_contacto character varying,
                                                                            c4_nexo_familiar character varying,
                                                                            c5_grado_instruccion character varying,
                                                                            c6_situacion_ocupacion character varying,
                                                                            c7_tipo_vivienda character varying,
                                                                            c8_tenencia_vivienda character varying,
                                                                            c9_personas_viven_usted integer,
                                                                            c10_personas_menores_6 integer,
                                                                            c11_personas_menores_6_12 integer,
                                                                            c12_personas_menores_6_12_escuela character varying,
                                                                            c13_frecuencia_escuela character varying,
                                                                            c14_personas_ingresos integer,
                                                                            c15_ingreso_hogar character varying,
                                                                            c16_principal_hogar character varying,
                                                                            c17_familia_exterior character varying,
                                                                            c18_ayuda_economica_exterior character varying,
                                                                            c20_comidas_diarias character varying,
                                                                            create_uid integer,
                                                                            create_date timestamp,
                                                                            write_uid integer,
                                                                            write_date timestamp )
                                            ON T1.write_date = T2.write_date 
                                AND T1.datos_jornada_calendario = T2.datos_jornada_calendario
                                AND T1.cedula = T2.cedula
                        WHERE  T1.write_date IS NULL
                                            AND T1.datos_jornada_calendario IS NULL
                                            AND T1.cedula IS NULL
                                """
            cur.execute(sql)
            if cur.rowcount > 0:
                list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %(NOMBRE_TABLA))
                campo_actualizar = cur.fetchall()
                descripcion = cur.description
                
                for update_casos_legal in campo_actualizar:
                    i = 0
                    sql = ' UPDATE  %s SET ' % (NOMBRE_TABLA)
                    for cd in descripcion:
                        if update_casos_legal[i] and (i != 42 and i != 44):
                            # print(cd.name)
                            if len(update_casos_legal) -1 == i:
                                sql = sql + cd.name + '=\'%s\'' % (update_casos_legal[i])
                                
                            else:
                                sql = sql + cd.name + '=\'%s\',' % (update_casos_legal[i])
                        i=i+1
                    sql = sql + ' WHERE datos_jornada_calendario=\'%s\' AND   cedula=\'%s\' AND create_date=\'%s\'' % (update_casos_legal[0],
                                                                                                                        update_casos_legal[5],
                                                                                                                        update_casos_legal[43])
                    cur.execute(sql)
                    if cur.rowcount > 0:
                        conexion.commit()
                        list_.append('Se actualizó el registro [CI: %s Nom: %s] de la tabla << %s >> en la PC local (%s)' %(update_casos_legal[5],update_casos_legal[2],NOMBRE_TABLA,cur.statusmessage))
                    else:
                        list_.append('No hubo actualización en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                #         self.ENTRAR_ACT_2 = False
                # list_.append('ENTRAR_ACT_2: %s' % (self.ENTRAR_ACT_2))
                sql = 'ALTER TABLE %s ENABLE TRIGGER ALL' % (NOMBRE_TABLA)
                cur.execute(sql)
                conexion.commit()
                list_.append('Se habilitaron los TRIGGER de la tabla << %s >> (%s)' %(NOMBRE_TABLA , cur.statusmessage))
                            
                list_.append('---------------------------------------------------------------------------------')

            else:
                list_.append('La consulta NO encontró diferencias entre la tabla << %s >> del Servidor y la PC local (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                self.ENTRAR_ACT_2 = False
                list_.append('ENTRAR_ACT_2: %s' % (self.ENTRAR_ACT_2))
        except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función action_actualizar_casos_legal_sin_campos_relacion' % (error, NOMBRE_TABLA))
        finally:
            cur.close()
            conexion.close()

    #1.3
    def action_actualizar_registro_asesoria_relacion_c19(self):
        NOMBRE_TABLA = 'public.registro_asesoria_registro_cuestionario1_c19_rel_aux'
        NOMBRE_TABLA_REAL = 'public.registro_asesoria_registro_cuestionario1_c19_rel'
        NOMBRE_FUNCION = 'action_actualizar_registro_asesoria_relacion_c19'
        list_.append('Inicio de la función # 1.3 << %s >>' % (NOMBRE_FUNCION))
        
        continuar_eje = True
        CONTINUAR_EJE_2 = True
        CONTINUAR_EJE_3 = 0

        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        USER_LOCAL="openpg"
        PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
            cur = conexion.cursor()
            sql = """ CREATE TABLE %s
                        (
                        A_id integer,
                        B_id integer,
                        cedula varchar
                        )
                """ % (NOMBRE_TABLA)
            cur.execute(sql)
            conexion.commit()
            continuar_eje = True
            list_.append('Se creó la tabla temporal << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            print(cur.statusmessage)    
                
        except (Exception, psycopg2.DatabaseError) as error:
            if error.pgcode != '42P07':
                continuar_eje = False
                list_.append('Error: %s. Al intentar crear la tabla temporal << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                print(error)
                    
        finally:
            cur.close()
            conexion.close()

        if continuar_eje:

            try:
                conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)
                cur = conexion.cursor()
                sql = 'DELETE FROM %s ' % (NOMBRE_TABLA)
                cur.execute(sql)
                conexion.commit()
                list_.append('Se limpió la información de la tabla temporal << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                print(cur.statusmessage)
            except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar limpiar la tabla << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                print(error)
            finally:
                cur.close()
                conexion.close()
            try:
                conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
                cur = conexion.cursor()
                sql = """ 	INSERT INTO %s
                                (A_id,B_id,cedula)
                            SELECT  T2.registro_asesoria_id, 
                                    T2.registro_cuestionario1_c19_id,
                                    T2.cedula							  
                            FROM  dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 
                                                                        'SELECT registro_asesoria_id,
                                                                            registro_cuestionario1_c19_id,
                                                                                        cedula
                                                                        FROM registro_asesoria_registro_cuestionario1_c19_rel RARCCR, registro_asesoria RA
                                                                            WHERE RARCCR.registro_asesoria_id = RA.id')
                                                                            AS t1( registro_asesoria_id integer ,registro_cuestionario1_c19_id integer, cedula varchar)
                            RIGHT JOIN
                                dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 
                                                                            'SELECT registro_asesoria_id,
                                                                                        registro_cuestionario1_c19_id,
                                                                                        cedula
                                                                            FROM registro_asesoria_registro_cuestionario1_c19_rel RARCCR, registro_asesoria RA
                                                                            WHERE RARCCR.registro_asesoria_id = RA.id')
                                                                            AS t2(registro_asesoria_id integer ,registro_cuestionario1_c19_id integer, cedula varchar)
                            ON T1.cedula = T2.cedula
                            WHERE T1.cedula IS NULL 
                    """ % (NOMBRE_TABLA)
                cur.execute(sql)
                if cur.rowcount > 0:
                    conexion.commit()
                    list_.append('Se insertó en la tabla temporal << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
                    CONTINUAR_EJE_2 = True
                else:
                    list_.append('No hubo inserciones en la tabla temporal << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                    CONTINUAR_EJE_2 = False
                print(cur.statusmessage)
            except (Exception, psycopg2.DatabaseError) as error:
                    list_.append('Error: %s. Al intentar insertar registros la tabla temporal << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                    print(error)
                    CONTINUAR_EJE_2 = False
            finally:
                cur.close()
                conexion.close()
        
            if CONTINUAR_EJE_2:
                # Actualizan los campos cuando en el Servidor hay un cambio, en caso contrario esta consulta es vacia
                try:
                    conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
                    cur = conexion.cursor()
                    sql = """ SELECT  T2.registro_asesoria_id, 
                                        T2.registro_cuestionario1_c19_id,
                                        T1.id,
                                        T2.id, 
                                        T2.datos_jornada_calendario,
                                T2.estatus,
                                T2.nombre,
                                T2.apellido,
                                T2.foto_carnet_clave,
                                T2.cedula,
                                T2.fecha_nacimiento,
                                T2.edad_,
                                T2.email,
                                T2.genero,
                                T2.estado_civil,
                                T2.nacionalidad,
                                T2.estado,
                                T2.municipio,
                                T2.parroquia,
                                T2.calle_callejon_av_trs,
                                T2.casa_edif,
                                T2.escalera,
                                T2.piso,
                                T2.apartamento,
                                T2.barrio_urb_zona,
                                T2.direccion,
                                T2.telefono_habitacion,
                                T2.telefono_celular,
                                T2.telefono_trabajo,
                                T2.hora_contacto,
                                T2.c4_nexo_familiar,
                                T2.c5_grado_instruccion,
                                T2.c6_situacion_ocupacion,
                                T2.c7_tipo_vivienda,
                                T2.c8_tenencia_vivienda,
                                T2.c9_personas_viven_usted,
                                T2.c10_personas_menores_6,
                                T2.c11_personas_menores_6_12,
                                T2.c12_personas_menores_6_12_escuela,
                                T2.c13_frecuencia_escuela,
                                T2.c14_personas_ingresos,
                                T2.c15_ingreso_hogar,
                                T2.c16_principal_hogar,
                                T2.c17_familia_exterior,
                                T2.c18_ayuda_economica_exterior,
                                T2.c20_comidas_diarias,
                                T2.create_uid,
                                T2.create_date,
                                T2.write_uid,
                                T2.write_date
                        FROM    dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 'SELECT    id  ,
                                                        datos_jornada_calendario,
                                                estatus,
                                                nombre,
                                                apellido,
                                                foto_carnet_clave,
                                                cedula,
                                                fecha_nacimiento,
                                                edad_,
                                                email,
                                                genero,
                                                estado_civil,
                                                nacionalidad,
                                                estado,
                                                municipio,
                                                parroquia,
                                                calle_callejon_av_trs,
                                                casa_edif,
                                                escalera,
                                                piso,
                                                apartamento,
                                                barrio_urb_zona,
                                                direccion,
                                                telefono_habitacion,
                                                telefono_celular,
                                                telefono_trabajo,
                                                hora_contacto,
                                                c4_nexo_familiar,
                                                c5_grado_instruccion,
                                                c6_situacion_ocupacion,
                                                c7_tipo_vivienda,
                                                c8_tenencia_vivienda,
                                                c9_personas_viven_usted,
                                                c10_personas_menores_6,
                                                c11_personas_menores_6_12,
                                                c12_personas_menores_6_12_escuela,
                                                c13_frecuencia_escuela,
                                                c14_personas_ingresos,
                                                c15_ingreso_hogar,
                                                c16_principal_hogar,
                                                c17_familia_exterior,
                                                c18_ayuda_economica_exterior,
                                                c20_comidas_diarias,
                                                create_uid,
                                                create_date,
                                                write_uid,
                                                write_date  
                                                FROM registro_asesoria')
                                                                                    AS t1(    id integer ,
                                                                                datos_jornada_calendario character varying,
                                                                                estatus character varying,
                                                                                nombre character varying,
                                                                                apellido character varying,
                                                                                foto_carnet_clave text,
                                                                                cedula character varying,
                                                                                fecha_nacimiento date,
                                                                                edad_ integer,
                                                                                email character varying,
                                                                                genero character varying,
                                                                                estado_civil character varying,
                                                                                nacionalidad integer,
                                                                                estado integer,
                                                                                municipio integer,
                                                                                parroquia integer,
                                                                                calle_callejon_av_trs character varying,
                                                                                casa_edif character varying,
                                                                                escalera character varying,
                                                                                piso character varying,
                                                                                apartamento character varying,
                                                                                barrio_urb_zona character varying,
                                                                                direccion text,
                                                                                telefono_habitacion character varying,
                                                                                telefono_celular character varying,
                                                                                telefono_trabajo character varying,
                                                                                hora_contacto character varying,
                                                                                c4_nexo_familiar character varying,
                                                                                c5_grado_instruccion character varying,
                                                                                c6_situacion_ocupacion character varying,
                                                                                c7_tipo_vivienda character varying,
                                                                                c8_tenencia_vivienda character varying,
                                                                                c9_personas_viven_usted integer,
                                                                                c10_personas_menores_6 integer,
                                                                                c11_personas_menores_6_12 integer,
                                                                                c12_personas_menores_6_12_escuela character varying,
                                                                                c13_frecuencia_escuela character varying,
                                                                                c14_personas_ingresos integer,
                                                                                c15_ingreso_hogar character varying,
                                                                                c16_principal_hogar character varying,
                                                                                c17_familia_exterior character varying,
                                                                                c18_ayuda_economica_exterior character varying,
                                                                                c20_comidas_diarias character varying,
                                                                                create_uid integer,
                                                                                create_date timestamp,
                                                                                write_uid integer,
                                                                                write_date timestamp  )
                            INNER JOIN
                                    dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 
                                                                'SELECT     CLIV.registro_asesoria_id, 
                                                                            CLIV.registro_cuestionario1_c19_id,
                                                                            id  ,
                                                                            datos_jornada_calendario,
                                                                            estatus,
                                                                            nombre,
                                                                            apellido,
                                                                            foto_carnet_clave,
                                                                            cedula,
                                                                            fecha_nacimiento,
                                                                            edad_,
                                                                            email,
                                                                            genero,
                                                                            estado_civil,
                                                                            nacionalidad,
                                                                            estado,
                                                                            municipio,
                                                                            parroquia,
                                                                            calle_callejon_av_trs,
                                                                            casa_edif,
                                                                            escalera,
                                                                            piso,
                                                                            apartamento,
                                                                            barrio_urb_zona,
                                                                            direccion,
                                                                            telefono_habitacion,
                                                                            telefono_celular,
                                                                            telefono_trabajo,
                                                                            hora_contacto,
                                                                            c4_nexo_familiar,
                                                                            c5_grado_instruccion,
                                                                            c6_situacion_ocupacion,
                                                                            c7_tipo_vivienda,
                                                                            c8_tenencia_vivienda,
                                                                            c9_personas_viven_usted,
                                                                            c10_personas_menores_6,
                                                                            c11_personas_menores_6_12,
                                                                            c12_personas_menores_6_12_escuela,
                                                                            c13_frecuencia_escuela,
                                                                            c14_personas_ingresos,
                                                                            c15_ingreso_hogar,
                                                                            c16_principal_hogar,
                                                                            c17_familia_exterior,
                                                                            c18_ayuda_economica_exterior,
                                                                            c20_comidas_diarias,
                                                                            create_uid,
                                                                            create_date,
                                                                            write_uid,
                                                                            write_date  
                                                                            FROM registro_asesoria CL, registro_asesoria_registro_cuestionario1_c19_rel CLIV
                                                                        WHERE CL.ID = CLIV.registro_asesoria_id')
                                                                    AS t2(    registro_asesoria_id integer, 
                                                                        registro_cuestionario1_c19_id integer,
                                                                        id integer ,
                                                                        datos_jornada_calendario character varying,
                                                                                estatus character varying,
                                                                                nombre character varying,
                                                                                apellido character varying,
                                                                                foto_carnet_clave text,
                                                                                cedula character varying,
                                                                                fecha_nacimiento date,
                                                                                edad_ integer,
                                                                                email character varying,
                                                                                genero character varying,
                                                                                estado_civil character varying,
                                                                                nacionalidad integer,
                                                                                estado integer,
                                                                                municipio integer,
                                                                                parroquia integer,
                                                                                calle_callejon_av_trs character varying,
                                                                                casa_edif character varying,
                                                                                escalera character varying,
                                                                                piso character varying,
                                                                                apartamento character varying,
                                                                                barrio_urb_zona character varying,
                                                                                direccion text,
                                                                                telefono_habitacion character varying,
                                                                                telefono_celular character varying,
                                                                                telefono_trabajo character varying,
                                                                                hora_contacto character varying,
                                                                                c4_nexo_familiar character varying,
                                                                                c5_grado_instruccion character varying,
                                                                                c6_situacion_ocupacion character varying,
                                                                                c7_tipo_vivienda character varying,
                                                                                c8_tenencia_vivienda character varying,
                                                                                c9_personas_viven_usted integer,
                                                                                c10_personas_menores_6 integer,
                                                                                c11_personas_menores_6_12 integer,
                                                                                c12_personas_menores_6_12_escuela character varying,
                                                                                c13_frecuencia_escuela character varying,
                                                                                c14_personas_ingresos integer,
                                                                                c15_ingreso_hogar character varying,
                                                                                c16_principal_hogar character varying,
                                                                                c17_familia_exterior character varying,
                                                                                c18_ayuda_economica_exterior character varying,
                                                                                c20_comidas_diarias character varying,
                                                                                create_uid integer,
                                                                                create_date timestamp,
                                                                                write_uid integer,
                                                                                write_date timestamp  )
                                ON T1.create_date = T2.create_date 
                                    AND T1.datos_jornada_calendario = T2.datos_jornada_calendario
                                    AND T1.cedula = T2.cedula

                                        """
                    cur.execute(sql)
                    if cur.rowcount > 0:
                        list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %('registro_asesoria'))
                        campo_actualizar = cur.fetchall()
                        descripcion = cur.description
                        CONTINUAR_EJE_3 = 0
                        
                        for update_casos_legal in campo_actualizar:
                            i = 0
                            sql = ' UPDATE  %s SET ' % (NOMBRE_TABLA)
                            for cd in descripcion:
                                if i == 0:
                                    # print(cd.name)
                                    sql = sql + 'A_id' + '=\'%s\'' % (update_casos_legal[2])
                                i=i+1
                            sql = sql + ' WHERE A_id=\'%s\' AND B_id=\'%s\' AND cedula=\'%s\'' % (update_casos_legal[0],update_casos_legal[1],update_casos_legal[9])
                            cur.execute(sql)
                            
                            if cur.rowcount > 0:
                                conexion.commit()
                                CONTINUAR_EJE_3 = CONTINUAR_EJE_3 + 1
                                list_.append('Se actualizó el registro [id: %s id: %s] de la tabla << %s >> en la PC local (%s)' %(update_casos_legal[0],update_casos_legal[1],NOMBRE_TABLA,cur.statusmessage))
                            else:
                                list_.append('No hubo actualización en la tabla << %s >> de la PC local  para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                        list_.append('---------------------------------------------------------------------------------')
                            # if cur.rowcount > 0:
                            #     conexion.commit()
                            #     CONTINUAR_EJE_3 = CONTINUAR_EJE_3 + 1
                            # print(cur.statusmessage)
                        
                    else:
                        list_.append('La consulta NO encontró diferencias entre la tabla << %s >> del Servidor y la PC local (%s)' %('registro_asesoria',cur.statusmessage))			
                        print(cur.statusmessage)
                except (Exception, psycopg2.DatabaseError) as error:
                        list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                        print(error)
                finally:
                    cur.close()
                    conexion.close()
                if CONTINUAR_EJE_3 > 0:
                    try:
                        conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)
                        cur = conexion.cursor()
                        sql = """ 	INSERT INTO %s
                                    SELECT  T2.registro_asesoria_id, T2.registro_cuestionario1_c19_id
                                    FROM    dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 'SELECT registro_asesoria_id,
                                                                                                registro_cuestionario1_c19_id
                                                                                    FROM %s')
                                                                                    AS t1(registro_asesoria_id integer ,registro_cuestionario1_c19_id integer)
                                    RIGHT JOIN
                                            dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 'SELECT A_id,
                                                                                    B_id 
                                                                                FROM %s')
                                                                                    AS t2( registro_asesoria_id integer ,registro_cuestionario1_c19_id integer)
                                        
                                    ON T1.registro_asesoria_id = T2.registro_asesoria_id
                                        AND T1.registro_cuestionario1_c19_id = T2.registro_cuestionario1_c19_id
                                    WHERE T1.registro_asesoria_id IS NULL 
                                            AND T1.registro_asesoria_id IS NULL  """ % (NOMBRE_TABLA_REAL, NOMBRE_TABLA_REAL ,NOMBRE_TABLA)
                        cur.execute(sql)
                        if cur.rowcount > 0:
                            conexion.commit()
                            list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA_REAL,cur.statusmessage))
                        else:
                            list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA_REAL,cur.statusmessage))
                        print(cur.statusmessage)
                            
                    except (Exception, psycopg2.DatabaseError) as error:
                        print(error)
                        list_.append('Error: (%s). Al intentar insertar en la tabla << %s >> en la función action_bajar_casos_legal' %(error, NOMBRE_TABLA_REAL))
                        _logger.info('Casos Legales action_actualizar_casos_legal........................................................................... 3 %s' % (error))
                
                    finally:
                        cur.close()
                        conexion.close()
                else:
                    list_.append("No habían datos en <<%s>> que actualizar" % (NOMBRE_TABLA))
            else:
                list_.append("No se puede continuar la TABLA << %s >> ¡ESTÁ VACÍA!" % (NOMBRE_TABLA_REAL))
            try:
                conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
                cur = conexion.cursor()
                sql = 'DROP TABLE %s ' % (NOMBRE_TABLA)
                cur.execute(sql)
                conexion.commit()
                # continuar_eje = True
                list_.append('Se Eliminó la tabla temporal << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                print(cur.statusmessage)   
                    
            except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar eliminar la tabla temporal << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                print(error)
            finally:
                cur.close()
                conexion.close()
        else:
            print("No se pudo continuar ejecutando esta función porque la TABLA PIVOTE << %s >> generó un error " %(NOMBRE_TABLA))        

    #1.4
    def action_actualizar_registro_asesoria_relacion_c21(self):
        NOMBRE_TABLA = 'public.registro_asesoria_registro_cuestionario1_c21_rel_aux'
        NOMBRE_TABLA_REAL = 'public.registro_asesoria_registro_cuestionario1_c21_rel'
        NOMBRE_FUNCION = 'action_actualizar_registro_asesoria_relacion_c21'
        list_.append('Inicio de la función # 1.4 << %s >>' % (NOMBRE_FUNCION))
        
        continuar_eje = True
        CONTINUAR_EJE_2 = True
        CONTINUAR_EJE_3 = 0

        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        USER_LOCAL="openpg"
        PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
            cur = conexion.cursor()
            sql = """ CREATE TABLE %s
                        (
                        A_id integer,
                        B_id integer,
                        cedula varchar
                        )
                """ % (NOMBRE_TABLA)
            cur.execute(sql)
            conexion.commit()
            continuar_eje = True
            list_.append('Se creó la tabla temporal << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            print(cur.statusmessage)    
                
        except (Exception, psycopg2.DatabaseError) as error:
            if error.pgcode != '42P07':
                continuar_eje = False
                list_.append('Error: %s. Al intentar crear la tabla temporal << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                print(error)
                    
        finally:
            cur.close()
            conexion.close()

        if continuar_eje:

            try:
                conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)
                cur = conexion.cursor()
                sql = 'DELETE FROM %s ' % (NOMBRE_TABLA)
                cur.execute(sql)
                conexion.commit()
                list_.append('Se limpió la información de la tabla temporal << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                print(cur.statusmessage)
            except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar limpiar la tabla << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                print(error)
            finally:
                cur.close()
                conexion.close()
            try:
                conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
                cur = conexion.cursor()
                sql = """ 	INSERT INTO %s
                                (A_id,B_id,cedula)
                            SELECT  T2.registro_asesoria_id, 
                                    T2.registro_cuestionario1_c21_id,
                                    T2.cedula                             
                            FROM  dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 
                                                                        'SELECT registro_asesoria_id,
                                                                                registro_cuestionario1_c21_id,
                                                                                cedula
                                                                        FROM registro_asesoria_registro_cuestionario1_c21_rel RARCCR, registro_asesoria RA
                                                                            WHERE RARCCR.registro_asesoria_id = RA.id')
                                                                            AS t1( registro_asesoria_id integer ,registro_cuestionario1_c21_id integer, cedula varchar)
                            RIGHT JOIN
                                dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 
                                                                            'SELECT registro_asesoria_id,
                                                                                    registro_cuestionario1_c21_id,
                                                                                    cedula
                                                                            FROM registro_asesoria_registro_cuestionario1_c21_rel RARCCR, registro_asesoria RA
                                                                            WHERE RARCCR.registro_asesoria_id = RA.id')
                                                                            AS t2(registro_asesoria_id integer ,registro_cuestionario1_c21_id integer, cedula varchar)
                            ON T1.cedula = T2.cedula
                            WHERE T1.cedula IS NULL 
                    """ % (NOMBRE_TABLA)
                cur.execute(sql)
                if cur.rowcount > 0:
                    conexion.commit()
                    list_.append('Se insertó en la tabla temporal << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
                    CONTINUAR_EJE_2 = True
                else:
                    list_.append('No hubo inserciones en la tabla temporal << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                    CONTINUAR_EJE_2 = False
                print(cur.statusmessage)
            except (Exception, psycopg2.DatabaseError) as error:
                    list_.append('Error: %s. Al intentar insertar registros la tabla temporal << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                    print(error)
                    CONTINUAR_EJE_2 = False
            finally:
                cur.close()
                conexion.close()
        
            if CONTINUAR_EJE_2:
                # Actualizan los campos cuando en el Servidor hay un cambio, en caso contrario esta consulta es vacia
                try:
                    conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
                    cur = conexion.cursor()
                    sql = """  SELECT  T2.registro_asesoria_id, 
                                        T2.registro_cuestionario1_c21_id,
                                        T1.id,
                                        T2.id, 
                                        T2.datos_jornada_calendario,
                                T2.estatus,
                                T2.nombre,
                                T2.apellido,
                                T2.foto_carnet_clave,
                                T2.cedula,
                                T2.fecha_nacimiento,
                                T2.edad_,
                                T2.email,
                                T2.genero,
                                T2.estado_civil,
                                T2.nacionalidad,
                                T2.estado,
                                T2.municipio,
                                T2.parroquia,
                                T2.calle_callejon_av_trs,
                                T2.casa_edif,
                                T2.escalera,
                                T2.piso,
                                T2.apartamento,
                                T2.barrio_urb_zona,
                                T2.direccion,
                                T2.telefono_habitacion,
                                T2.telefono_celular,
                                T2.telefono_trabajo,
                                T2.hora_contacto,
                                T2.c4_nexo_familiar,
                                T2.c5_grado_instruccion,
                                T2.c6_situacion_ocupacion,
                                T2.c7_tipo_vivienda,
                                T2.c8_tenencia_vivienda,
                                T2.c9_personas_viven_usted,
                                T2.c10_personas_menores_6,
                                T2.c11_personas_menores_6_12,
                                T2.c12_personas_menores_6_12_escuela,
                                T2.c13_frecuencia_escuela,
                                T2.c14_personas_ingresos,
                                T2.c15_ingreso_hogar,
                                T2.c16_principal_hogar,
                                T2.c17_familia_exterior,
                                T2.c18_ayuda_economica_exterior,
                                T2.c20_comidas_diarias,
                                T2.create_uid,
                                T2.create_date,
                                T2.write_uid,
                                T2.write_date
                        FROM    dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 'SELECT    id  ,
                                                        datos_jornada_calendario,
                                                estatus,
                                                nombre,
                                                apellido,
                                                foto_carnet_clave,
                                                cedula,
                                                fecha_nacimiento,
                                                edad_,
                                                email,
                                                genero,
                                                estado_civil,
                                                nacionalidad,
                                                estado,
                                                municipio,
                                                parroquia,
                                                calle_callejon_av_trs,
                                                casa_edif,
                                                escalera,
                                                piso,
                                                apartamento,
                                                barrio_urb_zona,
                                                direccion,
                                                telefono_habitacion,
                                                telefono_celular,
                                                telefono_trabajo,
                                                hora_contacto,
                                                c4_nexo_familiar,
                                                c5_grado_instruccion,
                                                c6_situacion_ocupacion,
                                                c7_tipo_vivienda,
                                                c8_tenencia_vivienda,
                                                c9_personas_viven_usted,
                                                c10_personas_menores_6,
                                                c11_personas_menores_6_12,
                                                c12_personas_menores_6_12_escuela,
                                                c13_frecuencia_escuela,
                                                c14_personas_ingresos,
                                                c15_ingreso_hogar,
                                                c16_principal_hogar,
                                                c17_familia_exterior,
                                                c18_ayuda_economica_exterior,
                                                c20_comidas_diarias,
                                                create_uid,
                                                create_date,
                                                write_uid,
                                                write_date  
                                                FROM registro_asesoria')
                                                                                    AS t1(    id integer ,
                                                                                datos_jornada_calendario character varying,
                                                                                estatus character varying,
                                                                                nombre character varying,
                                                                                apellido character varying,
                                                                                foto_carnet_clave text,
                                                                                cedula character varying,
                                                                                fecha_nacimiento date,
                                                                                edad_ integer,
                                                                                email character varying,
                                                                                genero character varying,
                                                                                estado_civil character varying,
                                                                                nacionalidad integer,
                                                                                estado integer,
                                                                                municipio integer,
                                                                                parroquia integer,
                                                                                calle_callejon_av_trs character varying,
                                                                                casa_edif character varying,
                                                                                escalera character varying,
                                                                                piso character varying,
                                                                                apartamento character varying,
                                                                                barrio_urb_zona character varying,
                                                                                direccion text,
                                                                                telefono_habitacion character varying,
                                                                                telefono_celular character varying,
                                                                                telefono_trabajo character varying,
                                                                                hora_contacto character varying,
                                                                                c4_nexo_familiar character varying,
                                                                                c5_grado_instruccion character varying,
                                                                                c6_situacion_ocupacion character varying,
                                                                                c7_tipo_vivienda character varying,
                                                                                c8_tenencia_vivienda character varying,
                                                                                c9_personas_viven_usted integer,
                                                                                c10_personas_menores_6 integer,
                                                                                c11_personas_menores_6_12 integer,
                                                                                c12_personas_menores_6_12_escuela character varying,
                                                                                c13_frecuencia_escuela character varying,
                                                                                c14_personas_ingresos integer,
                                                                                c15_ingreso_hogar character varying,
                                                                                c16_principal_hogar character varying,
                                                                                c17_familia_exterior character varying,
                                                                                c18_ayuda_economica_exterior character varying,
                                                                                c20_comidas_diarias character varying,
                                                                                create_uid integer,
                                                                                create_date timestamp,
                                                                                write_uid integer,
                                                                                write_date timestamp  )
                            INNER JOIN
                                    dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 
                                                                'SELECT     CLIV.registro_asesoria_id, 
                                                                            CLIV.registro_cuestionario1_c21_id,
                                                                            id  ,
                                                                            datos_jornada_calendario,
                                                                            estatus,
                                                                            nombre,
                                                                            apellido,
                                                                            foto_carnet_clave,
                                                                            cedula,
                                                                            fecha_nacimiento,
                                                                            edad_,
                                                                            email,
                                                                            genero,
                                                                            estado_civil,
                                                                            nacionalidad,
                                                                            estado,
                                                                            municipio,
                                                                            parroquia,
                                                                            calle_callejon_av_trs,
                                                                            casa_edif,
                                                                            escalera,
                                                                            piso,
                                                                            apartamento,
                                                                            barrio_urb_zona,
                                                                            direccion,
                                                                            telefono_habitacion,
                                                                            telefono_celular,
                                                                            telefono_trabajo,
                                                                            hora_contacto,
                                                                            c4_nexo_familiar,
                                                                            c5_grado_instruccion,
                                                                            c6_situacion_ocupacion,
                                                                            c7_tipo_vivienda,
                                                                            c8_tenencia_vivienda,
                                                                            c9_personas_viven_usted,
                                                                            c10_personas_menores_6,
                                                                            c11_personas_menores_6_12,
                                                                            c12_personas_menores_6_12_escuela,
                                                                            c13_frecuencia_escuela,
                                                                            c14_personas_ingresos,
                                                                            c15_ingreso_hogar,
                                                                            c16_principal_hogar,
                                                                            c17_familia_exterior,
                                                                            c18_ayuda_economica_exterior,
                                                                            c20_comidas_diarias,
                                                                            create_uid,
                                                                            create_date,
                                                                            write_uid,
                                                                            write_date  
                                                                            FROM registro_asesoria CL, registro_asesoria_registro_cuestionario1_c21_rel CLIV
                                                                        WHERE CL.ID = CLIV.registro_asesoria_id')
                                                                    AS t2(    registro_asesoria_id integer, 
                                                                        registro_cuestionario1_c21_id integer,
                                                                        id integer ,
                                                                        datos_jornada_calendario character varying,
                                                                                estatus character varying,
                                                                                nombre character varying,
                                                                                apellido character varying,
                                                                                foto_carnet_clave text,
                                                                                cedula character varying,
                                                                                fecha_nacimiento date,
                                                                                edad_ integer,
                                                                                email character varying,
                                                                                genero character varying,
                                                                                estado_civil character varying,
                                                                                nacionalidad integer,
                                                                                estado integer,
                                                                                municipio integer,
                                                                                parroquia integer,
                                                                                calle_callejon_av_trs character varying,
                                                                                casa_edif character varying,
                                                                                escalera character varying,
                                                                                piso character varying,
                                                                                apartamento character varying,
                                                                                barrio_urb_zona character varying,
                                                                                direccion text,
                                                                                telefono_habitacion character varying,
                                                                                telefono_celular character varying,
                                                                                telefono_trabajo character varying,
                                                                                hora_contacto character varying,
                                                                                c4_nexo_familiar character varying,
                                                                                c5_grado_instruccion character varying,
                                                                                c6_situacion_ocupacion character varying,
                                                                                c7_tipo_vivienda character varying,
                                                                                c8_tenencia_vivienda character varying,
                                                                                c9_personas_viven_usted integer,
                                                                                c10_personas_menores_6 integer,
                                                                                c11_personas_menores_6_12 integer,
                                                                                c12_personas_menores_6_12_escuela character varying,
                                                                                c13_frecuencia_escuela character varying,
                                                                                c14_personas_ingresos integer,
                                                                                c15_ingreso_hogar character varying,
                                                                                c16_principal_hogar character varying,
                                                                                c17_familia_exterior character varying,
                                                                                c18_ayuda_economica_exterior character varying,
                                                                                c20_comidas_diarias character varying,
                                                                                create_uid integer,
                                                                                create_date timestamp,
                                                                                write_uid integer,
                                                                                write_date timestamp  )
                                ON T1.create_date = T2.create_date 
                                    AND T1.datos_jornada_calendario = T2.datos_jornada_calendario
                                    AND T1.cedula = T2.cedula """
                    cur.execute(sql)
                    if cur.rowcount > 0:
                        list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %('registro_asesoria'))
                        campo_actualizar = cur.fetchall()
                        descripcion = cur.description
                        CONTINUAR_EJE_3 = 0
                        
                        for update_casos_legal in campo_actualizar:
                            i = 0
                            sql = ' UPDATE  %s SET ' % (NOMBRE_TABLA)
                            for cd in descripcion:
                                if i == 0:
                                    # print(cd.name)
                                    sql = sql + 'A_id' + '=\'%s\'' % (update_casos_legal[2])
                                i=i+1
                            sql = sql + ' WHERE A_id=\'%s\' AND B_id=\'%s\' AND cedula=\'%s\'' % (update_casos_legal[0],update_casos_legal[1],update_casos_legal[9])
                            cur.execute(sql)
                            
                            if cur.rowcount > 0:
                                conexion.commit()
                                CONTINUAR_EJE_3 = CONTINUAR_EJE_3 + 1
                                list_.append('Se actualizó el registro [id: %s id: %s] de la tabla << %s >> en la PC local (%s)' %(update_casos_legal[0],update_casos_legal[1],NOMBRE_TABLA,cur.statusmessage))
                            else:
                                list_.append('No hubo actualización en la tabla << %s >> de la PC local  para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                        list_.append('---------------------------------------------------------------------------------')
                            # if cur.rowcount > 0:
                            #     conexion.commit()
                            #     CONTINUAR_EJE_3 = CONTINUAR_EJE_3 + 1
                            # print(cur.statusmessage)
                        
                    else:
                        list_.append('La consulta NO encontró diferencias entre la tabla << %s >> del Servidor y la PC local (%s)' %(NOMBRE_TABLA,cur.statusmessage))			
                        print(cur.statusmessage)
                except (Exception, psycopg2.DatabaseError) as error:
                        list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                        print(error)
                finally:
                    cur.close()
                    conexion.close()
                if CONTINUAR_EJE_3 > 0:
                    try:
                        conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)
                        cur = conexion.cursor()
                        sql = """ 	INSERT INTO %s
                                    SELECT  T2.registro_asesoria_id, T2.registro_cuestionario1_c21_id
                                    FROM    dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 'SELECT registro_asesoria_id,
                                                                                                registro_cuestionario1_c21_id
                                                                                    FROM %s')
                                                                                    AS t1(registro_asesoria_id integer ,registro_cuestionario1_c21_id integer)
                                    RIGHT JOIN
                                            dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 'SELECT A_id,
                                                                                    B_id 
                                                                                FROM %s')
                                                                                    AS t2( registro_asesoria_id integer ,registro_cuestionario1_c21_id integer)
                                        
                                    ON T1.registro_asesoria_id = T2.registro_asesoria_id
                                        AND T1.registro_cuestionario1_c21_id = T2.registro_cuestionario1_c21_id
                                    WHERE T1.registro_asesoria_id IS NULL 
                                            AND T1.registro_asesoria_id IS NULL  """ % (NOMBRE_TABLA_REAL, NOMBRE_TABLA_REAL ,NOMBRE_TABLA)
                        cur.execute(sql)
                        if cur.rowcount > 0:
                            conexion.commit()
                            list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA_REAL,cur.statusmessage))
                        else:
                            list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA_REAL,cur.statusmessage))
                        print(cur.statusmessage)
                            
                    except (Exception, psycopg2.DatabaseError) as error:
                        print(error)
                        list_.append('Error: (%s). Al intentar insertar en la tabla << %s >> en la función action_bajar_casos_legal' %(error, NOMBRE_TABLA_REAL))
                        _logger.info('Casos Legales action_actualizar_casos_legal........................................................................... 3 %s' % (error))
                
                    finally:
                        cur.close()
                        conexion.close()
                else:
                    list_.append("No habían datos en <<%s>> que actualizar" % (NOMBRE_TABLA))
            else:
                list_.append("No se puede continuar la TABLA << %s >> ¡ESTÁ VACÍA!" %(NOMBRE_TABLA))
            try:
                conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
                cur = conexion.cursor()
                sql = 'DROP TABLE %s ' % (NOMBRE_TABLA)
                cur.execute(sql)
                conexion.commit()
                # continuar_eje = True
                list_.append('Se Eliminó la tabla temporal << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                print(cur.statusmessage)   
                    
            except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar eliminar la tabla temporal << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                print(error)
            finally:
                cur.close()
                conexion.close()
        else:
            print("No se pudo continuar ejecutando esta función porque la TABLA PIVOTE << %s >> generó un error " % (NOMBRE_TABLA))        

    #1.5 
    def action_actualizar_registro_asesoria_write_uid(self):
        NOMBRE_TABLA = 'public.registro_asesoria'
        # NOMBRE_TABLA_REAL = 'public.registro_asesoria_registro_cuestionario1_c21_rel'
        NOMBRE_FUNCION = 'action_actualizar_registro_asesoria_write_uid'
        list_.append('Inicio de la función # 1.5 << %s >>' % (NOMBRE_FUNCION))

        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        USER_LOCAL="openpg"
        PASSWORD_LOCAL="openpgpwd"
        try:
            conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
            cur = conexion.cursor()
            cr = self.env.cr
            sql = """  	SELECT t2.write_uid, t1.id, t2.datos_jornada_calendario, t2.create_date
                        FROM  	dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 
                                    'SELECT  	id  ,
                                                login
                                    FROM res_users') AS t1( id integer ,
                                                            login varchar)
                        INNER JOIN
                                dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 
                                        'SELECT ru.login,
                                                cl.id  ,
                                                datos_jornada_calendario, 
                                                cedula, 
                                                cl.create_uid , 
                                                cl.create_date, 
                                                cl.write_uid , 
                                                cl.write_date    
                                        FROM res_users ru,registro_asesoria cl
                                        WHERE  ru.id = cl.write_uid') AS t2(  login varchar,
                                                                                        id integer ,
                                                                                        datos_jornada_calendario varchar, 
                                                                                        cedula varchar,  
                                                                                        create_uid integer, 
                                                                                        create_date timestamp, 
                                                                                        write_uid integer, 
                                                                                        write_date timestamp )
                        ON T1.login = T2.login
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
                    sql = sql + '\' UPDATE  %s SET ' % (NOMBRE_TABLA)
                    for cd in descripcion:
                        if i == 0:
                            # print(cd.name)
                            sql = sql + cd.name + '=\'\'%s\'\'' % (update_casos_legal[1])
                        i=i+1
                    sql = sql + ' WHERE datos_jornada_calendario=\'\'%s\'\' AND create_date=\'\'%s\'\' \' )' % (update_casos_legal[2],	update_casos_legal[3])
                    cr.execute(sql)
                    if cr.rowcount > 0 :
                        # conexion.commit()
                        list_.append('Se actualizó el registro [Write id.: %s Datos Jornada: %s] de la tabla << %s >> en la PC local (%s)' %(update_casos_legal[1],update_casos_legal[2],NOMBRE_TABLA,cr.statusmessage))
                    else:
                        list_.append('No hubo actualización en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cr.statusmessage))
                list_.append('---------------------------------------------------------------------------------')
            else:
                list_.append('La consulta NO encontró diferencias entre la tabla << %s >> del Servidor y la PC local (%s)' %(NOMBRE_TABLA,cur.statusmessage))			
                _logger.info('........................................................................... 2 %s' % (cur.statusmessage))
                
        except (Exception, psycopg2.DatabaseError) as error:
            list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA,NOMBRE_FUNCION))
            _logger.info('........................................................................... 3 %s' % (error))
                
        finally:
            cur.close()
            conexion.close()
            
        # mostrar_resultados_update()

    #1
    def action_actualizar_registro_asesoria_completamente(self):
        
        try:
            self.ENTRAR_ACT_1 = True
            self.ENTRAR_ACT_2 = True
            
            # 2.1
            self.action_bajar_registro_asesoria_y_create_uid()
            list_.append('Salió de la función << action_bajar_registro_asesoria_y_create_uid >>')
            
            # 2.2
            self.action_actualizar_registro_asesoria_sin_campos_relacion()
            list_.append('Salió de la función << action_actualizar_registro_asesoria_sin_campos_relacion >>')
            
            if self.ENTRAR_ACT_1 or self.ENTRAR_ACT_2:
                # 2.3
                self.action_actualizar_registro_asesoria_relacion_c19()
                list_.append('Salió de la función << action_actualizar_registro_asesoria_relacion_c19 >>')
                    
                # 1.4
                self.action_actualizar_registro_asesoria_relacion_c21()
                list_.append('Salió de la función << action_actualizar_registro_asesoria_relacion_c21 >>')
                    
                # 1.5
                self.action_actualizar_registro_asesoria_write_uid()
                list_.append('Salió de la función << action_actualizar_registro_asesoria_write_uid >>')

            # 0.1
            self.mostrar_resultados_update()
            
        except (Exception, psycopg2.DatabaseError) as error:
            list_.append('Error: %s. al intentar actualizar la tabla << registro_asesoria >> por COMPLETO del PC Local' %(error))
            # _logger.info('........................................................................... 3 action_actualizar_casos_legal_completamente %s' % (error))
            self.mostrar_resultados_update()
    
    #2.1
    def action_bajar_casos_legal_create_y_write_uid(self):
        
        continuar_eje = True
        CONTINUAR_EJE_2 = True
        CONTINUAR_EJE_3 = 0
        NOMBRE_TABLA = 'public.casos_legal_aux'
        NOMBRE_FUNCION = 'action_bajar_casos_legal_create_y_write_uid'
    
        list_.append('Inicio de la función # 2.1 << %s >>' % (NOMBRE_FUNCION))

        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        USER_LOCAL="openpg"
        PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
            cur = conexion.cursor()
            sql = """ CREATE TABLE %s
                        (
                        id integer ,
                        login varchar,
                        datos_jornada_calendario varchar, 
                        estatus varchar,
                        cedula varchar, 
                        nombre varchar, 
                        apellido varchar, 
                        observaciones_caso text, 
                        tripulante_asignado integer, 
                        recaudos_recibidos varchar, 
                        fecha_documento_entregado date, 
                        datos_asesoria integer, 
                        descripcion_asesoria text, 
                        cedula_parte2 varchar, 
                        nombre_parte2 varchar, 
                        direccion_parte2 text, 
                        fecha_citacion date, 
                        categoria_area_legal varchar, 
                        create_uid integer, 
                        create_date timestamp, 
                        write_uid integer, 
                        write_date timestamp  
                        )
                """ % (NOMBRE_TABLA)
            cur.execute(sql)
            conexion.commit()
            continuar_eje = True
            list_.append('Se creó la tabla temporal << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            _logger.info('........................................................................................................1 %s' % (cur.statusmessage))    
                
        except (Exception, psycopg2.DatabaseError) as error:
            if error.pgcode != '42P07':
                continuar_eje = False
                list_.append('Error: %s. Al intentar crear la tabla temporal << %s >> con la función %s' % (error, NOMBRE_TABLA, NOMBRE_FUNCION))
                _logger.info('....................................................................................................3 %s' % (error))
                mostrar_resultados_update(list_)

        finally:
            cur.close()
            conexion.close()

        if continuar_eje:

            try:
                conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)
                cur = conexion.cursor()
                sql = 'DELETE FROM %s ' % (NOMBRE_TABLA)
                cur.execute(sql)
                conexion.commit()
                list_.append('Se limpió la información de la tabla temporal << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                _logger.info('....................................................................................................1 %s' % (cur.statusmessage))
            except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar limpiar la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA , NOMBRE_FUNCION))
                mostrar_resultados_update(list_)
                _logger.info('....................................................................................................3 %s' % (error))
            finally:
                cur.close()
                conexion.close()
            try:
                conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
                cur = conexion.cursor()
                sql = """ 	INSERT INTO %s 
                                    (id,
                                    login,
                                    datos_jornada_calendario, 
                                    estatus,
                                    cedula, 
                                    nombre, 
                                    apellido, 
                                    observaciones_caso, 
                                    tripulante_asignado , 
                                    recaudos_recibidos, 
                                    fecha_documento_entregado, 
                                    datos_asesoria , 
                                    descripcion_asesoria, 
                                    cedula_parte2, 
                                    nombre_parte2, 
                                    direccion_parte2, 
                                    fecha_citacion, 
                                    categoria_area_legal, 
                                    create_uid , 
                                    create_date, 
                                    write_uid , 
                                    write_date )
                            SELECT 	RU.id, 
                                    T3.login,
                                    T3.datos_jornada_calendario, 
                                    T3.estatus,
                                    T3.cedula, 
                                    T3.nombre, 
                                    T3.apellido, 
                                    T3.observaciones_caso, 
                                    T3.tripulante_asignado , 
                                    T3.recaudos_recibidos, 
                                    T3.fecha_documento_entregado, 
                                    T3.datos_asesoria , 
                                    T3.descripcion_asesoria, 
                                    T3.cedula_parte2, 
                                    T3.nombre_parte2, 
                                    T3.direccion_parte2, 
                                    T3.fecha_citacion, 
                                    T3.categoria_area_legal, 
                                    T3.create_uid , 
                                    T3.create_date, 
                                    T3.write_uid , 
                                    T3.write_date
                            FROM (	SELECT	T2.login,
                                            T2.datos_jornada_calendario, 
                                            T2.estatus,
                                            T2.cedula, 
                                            T2.nombre, 
                                            T2.apellido, 
                                            T2.observaciones_caso, 
                                            T2.tripulante_asignado , 
                                            T2.recaudos_recibidos, 
                                            T2.fecha_documento_entregado, 
                                            T2.datos_asesoria , 
                                            T2.descripcion_asesoria, 
                                            T2.cedula_parte2, 
                                            T2.nombre_parte2, 
                                            T2.direccion_parte2, 
                                            T2.fecha_citacion, 
                                            T2.categoria_area_legal, 
                                            T2.create_uid , 
                                            T2.create_date, 
                                            T2.write_uid , 
                                            T2.write_date
                                    FROM  dblink(   'host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 
                                                    'SELECT id  ,
                                                            datos_jornada_calendario, 
                                                            estatus,
                                                            cedula, 
                                                            nombre, 
                                                            apellido, 
                                                            observaciones_caso, 
                                                            tripulante_asignado , 
                                                            recaudos_recibidos, 
                                                            fecha_documento_entregado, 
                                                            datos_asesoria , 
                                                            descripcion_asesoria, 
                                                            cedula_parte2, 
                                                            nombre_parte2, 
                                                            direccion_parte2, 
                                                            fecha_citacion, 
                                                            categoria_area_legal, 
                                                            create_uid , 
                                                            create_date, 
                                                            write_uid , 
                                                            write_date    
                                                            FROM casos_legal')  AS t1(id integer ,
                                                                                            datos_jornada_calendario varchar, 
                                                                                            estatus varchar,
                                                                                            cedula varchar, 
                                                                                            nombre varchar, 
                                                                                            apellido varchar, 
                                                                                            observaciones_caso text, 
                                                                                            tripulante_asignado integer, 
                                                                                            recaudos_recibidos varchar, 
                                                                                            fecha_documento_entregado date, 
                                                                                            datos_asesoria integer, 
                                                                                            descripcion_asesoria text, 
                                                                                            cedula_parte2 varchar, 
                                                                                            nombre_parte2 varchar, 
                                                                                            direccion_parte2 text, 
                                                                                            fecha_citacion date, 
                                                                                            categoria_area_legal varchar, 
                                                                                            create_uid integer, 
                                                                                            create_date timestamp, 
                                                                                            write_uid integer, 
                                                                                            write_date timestamp )
                                    RIGHT JOIN dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 
                                                    'SELECT   RU.login, 
                                                                CL.id  ,
                                                                datos_jornada_calendario, 
                                                                estatus,
                                                                cedula, 
                                                                nombre, 
                                                                apellido, 
                                                                observaciones_caso, 
                                                                tripulante_asignado , 
                                                                recaudos_recibidos, 
                                                                fecha_documento_entregado, 
                                                                datos_asesoria , 
                                                                descripcion_asesoria, 
                                                                cedula_parte2, 
                                                                nombre_parte2, 
                                                                direccion_parte2, 
                                                                fecha_citacion, 
                                                                categoria_area_legal, 
                                                                CL.create_uid , 
                                                                CL.create_date, 
                                                                CL.write_uid , 
                                                                CL.write_date    
                                                        FROM casos_legal CL, res_users RU
                                                        WHERE CL.create_uid = RU.id')  AS t2(login varchar,
                                                                                                id integer ,
                                                                                                datos_jornada_calendario varchar, 
                                                                                                estatus varchar,
                                                                                                cedula varchar, 
                                                                                                nombre varchar, 
                                                                                                apellido varchar, 
                                                                                                observaciones_caso text, 
                                                                                                tripulante_asignado integer, 
                                                                                                recaudos_recibidos varchar, 
                                                                                                fecha_documento_entregado date, 
                                                                                                datos_asesoria integer, 
                                                                                                descripcion_asesoria text, 
                                                                                                cedula_parte2 varchar, 
                                                                                                nombre_parte2 varchar, 
                                                                                                direccion_parte2 text, 
                                                                                                fecha_citacion date, 
                                                                                                categoria_area_legal varchar, 
                                                                                                create_uid integer, 
                                                                                                create_date timestamp, 
                                                                                                write_uid integer, 
                                                                                                write_date timestamp )
                                                    ON T1.create_date = T2.create_date
                                                    WHERE T1.create_date IS NULL ) T3, res_users RU
                            WHERE T3.LOGIN = RU.LOGIN
                    """ % (NOMBRE_TABLA)
                cur.execute(sql)
                if cur.rowcount > 0:
                    conexion.commit()
                    list_.append('Se insertó en la tabla temporal << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
                    CONTINUAR_EJE_2 = True
                else:
                    list_.append('No hubo inserciones en la tabla temporal << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                    CONTINUAR_EJE_2 = False
                # _logger.info('..................................................................' + cur.statusmessage)
            except (Exception, psycopg2.DatabaseError) as error:
                    list_.append('Error: %s. Al intentar insertar registros la tabla temporal << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                    _logger.info('....................................................................................................3 %s' % (error))
                    CONTINUAR_EJE_2 = False
            finally:
                cur.close()
                conexion.close()

            if CONTINUAR_EJE_2:
                # Actualizan los campos cuando en el Servidor hay un cambio, en caso contrario esta consulta es vacia
                try:
                    conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
                    cur = conexion.cursor()
                    sql = 	"""	SELECT *
                                FROM %s
                            """ % (NOMBRE_TABLA)
                    cur.execute(sql)
                    if cur.rowcount > 0:
                        list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %('casos_legal'))
                        campo_actualizar = cur.fetchall()
                        descripcion = cur.description
                        CONTINUAR_EJE_3 = 0
                        
                        for update_casos_legal in campo_actualizar:
                            i = 0
                            sql = ' UPDATE  %s SET ' % (NOMBRE_TABLA)
                            for cd in descripcion:
                                if update_casos_legal[i]:
                                    if 18 == i:
                                        sql = sql + cd.name + '=\'%s\'' % (update_casos_legal[0])
                                i=i+1
                            sql = sql + ' WHERE cedula=\'%s\' AND datos_jornada_calendario=\'%s\' AND categoria_area_legal=\'%s\' AND create_date=\'%s\'' % (update_casos_legal[4],
                                                                                                                                                            update_casos_legal[2],
                                                                                                                                                            update_casos_legal[17],
                                                                                                                                                            update_casos_legal[19])
                            cur.execute(sql)
                            
                            if cur.rowcount > 0:
                                conexion.commit()
                                CONTINUAR_EJE_3 = CONTINUAR_EJE_3 + 1
                                list_.append('Se actualizó el registro [CI: %s Nom.: %s] de la tabla << %s >> en la PC local (%s)' %(update_casos_legal[4],update_casos_legal[5],NOMBRE_TABLA,cur.statusmessage))
                            else:
                                list_.append('No hubo actualización en la tabla << %s >> de la PC local  para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                        list_.append('------------------------------------------------------------------------------------------------------------')
                    else:
                        list_.append('La consulta NO encontró diferencias entre la tabla << %s >> del Servidor y la PC local (%s)' %('casos_legal',cur.statusmessage))			
                        print(cur.statusmessage)
                except (Exception, psycopg2.DatabaseError) as error:
                        list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                        _logger.info('....................................................................................................3 %s' % (error))
                finally:
                    cur.close()
                    conexion.close()
                    
                if CONTINUAR_EJE_3 > 0:
                    
                    try:
                        conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)
                        cur = conexion.cursor()
                        
                        sql = 'ALTER TABLE casos_legal DISABLE TRIGGER ALL'
                        cur.execute(sql)
                        conexion.commit()
                        list_.append('Se deshabilitaron los TRIGGER de la tabla << casos_legal >> (%s)' %(cur.statusmessage))
                        
                        sql = """ 	INSERT INTO casos_legal 
                                        (datos_jornada_calendario, 
                                        estatus,
                                        cedula, 
                                        nombre, 
                                        apellido, 
                                        observaciones_caso, 
                                        tripulante_asignado , 
                                        recaudos_recibidos, 
                                        fecha_documento_entregado, 
                                        datos_asesoria , 
                                        descripcion_asesoria, 
                                        cedula_parte2, 
                                        nombre_parte2, 
                                        direccion_parte2, 
                                        fecha_citacion, 
                                        categoria_area_legal, 
                                        create_uid , 
                                        create_date, 
                                        write_uid , 
                                        write_date )
                                    SELECT 		T3.datos_jornada_calendario, 
                                            T3.estatus,
                                            T3.cedula, 
                                            T3.nombre, 
                                            T3.apellido, 
                                            T3.observaciones_caso, 
                                            T3.tripulante_asignado , 
                                            T3.recaudos_recibidos, 
                                            T3.fecha_documento_entregado, 
                                            T3.datos_asesoria , 
                                            T3.descripcion_asesoria, 
                                            T3.cedula_parte2, 
                                            T3.nombre_parte2, 
                                            T3.direccion_parte2, 
                                            T3.fecha_citacion, 
                                            T3.categoria_area_legal, 
                                            T3.create_uid , 
                                            T3.create_date, 
                                            T3.write_uid , 
                                            T3.write_date
                                    FROM 	%s T3""" % (NOMBRE_TABLA)
                        cur.execute(sql)
                        if cur.rowcount > 0:
                            conexion.commit()
                            list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %('casos_legal',cur.statusmessage))
                        else:
                            list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %('casos_legal',cur.statusmessage))
                        print(cur.statusmessage)
                        
                        sql = 'ALTER TABLE casos_legal ENABLE TRIGGER ALL'
                        cur.execute(sql)
                        conexion.commit()
                        list_.append('Se habilitaron los TRIGGER de la tabla << casos_legal >> (%s)' %(cur.statusmessage))
                            
                    except (Exception, psycopg2.DatabaseError) as error:
                        print(error)
                        list_.append('Error: (%s). Al intentar insertar en la tabla << %s >> en la función action_bajar_casos_legal' %(error, 'casos_legal'))
                        _logger.info('Casos Legales ........................................................................... 3 %s' % (error))
                        self.ENTRAR_ACT_1 = False
                        list_.append('ENTRAR_ACT_1: %s' % (self.ENTRAR_ACT_1))
                    finally:
                        cur.close()
                        conexion.close()
                else:
                    list_.append("No habían datos en <<%s>> que actualizar" % (NOMBRE_TABLA))
                    self.ENTRAR_ACT_1 = False
                    list_.append('ENTRAR_ACT_1: %s' % (self.ENTRAR_ACT_1))
            else:
                list_.append("No se puede continuar porque la TABLA << %s >> ¡ESTÁ VACÍA!" % (NOMBRE_TABLA))
                self.ENTRAR_ACT_1 = False
                list_.append('ENTRAR_ACT_1: %s' % (self.ENTRAR_ACT_1))
            try:
                conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
                cur = conexion.cursor()
                sql = 'DROP TABLE %s ' % (NOMBRE_TABLA)
                cur.execute(sql)
                conexion.commit()
                # continuar_eje = True
                list_.append('Se Eliminó la tabla temporal << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                print(cur.statusmessage)   
                    
            except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar eliminar la tabla temporal << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                _logger.info('Casos Legales ........................................................................... 3 %s' % (error))
                self.ENTRAR_ACT_1 = False
                list_.append('ENTRAR_ACT_1: %s' % (self.ENTRAR_ACT_1))
            finally:
                cur.close()
                conexion.close()
        else:
            list_.append("No se pudo continuar ejecutando esta función porque la TABLA PIVOTE << %s >> generó un error " % (NOMBRE_TABLA))
            self.ENTRAR_ACT_1 = False
            list_.append('ENTRAR_ACT_1: %s' % (self.ENTRAR_ACT_1))
        
        # self.mostrar_resultados_update()

    #2.2
    def action_actualizar_casos_legal_sin_campos_relacion(self):
        list_.append('Inicio de la función # 2.2 << action_actualizar_casos_legal_sin_campos_relacion >>')

        NOMBRE_TABLA = 'public.casos_legal'

        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        USER_LOCAL="openpg"
        PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
            cur = conexion.cursor()
            sql = """  	SELECT	 				T2.datos_jornada_calendario, 
                                                T2.estatus,
                                                T2.cedula, 
                                                T2.nombre, 
                                                T2.apellido, 
                                                T2.observaciones_caso, 
                                                T2.tripulante_asignado , 
                                                T2.recaudos_recibidos, 
                                                T2.fecha_documento_entregado, 
                                                T2.datos_asesoria , 
                                                T2.descripcion_asesoria, 
                                                T2.cedula_parte2, 
                                                T2.nombre_parte2, 
                                                T2.direccion_parte2, 
                                                T2.fecha_citacion, 
                                                T2.categoria_area_legal, 
                                                T2.create_uid , 
                                                T2.create_date, 
                                                T2.write_uid , 
                                                T2.write_date
                                    FROM  	dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 'SELECT    id  ,
                                                                datos_jornada_calendario, 
                                                                estatus,
                                                                cedula, 
                                                                nombre, 
                                                                apellido, 
                                                                observaciones_caso, 
                                                                tripulante_asignado , 
                                                                recaudos_recibidos, 
                                                                fecha_documento_entregado, 
                                                                datos_asesoria , 
                                                                descripcion_asesoria, 
                                                                cedula_parte2, 
                                                                nombre_parte2, 
                                                                direccion_parte2, 
                                                                fecha_citacion, 
                                                                categoria_area_legal, 
                                                                create_uid , 
                                                                create_date, 
                                                                write_uid , 
                                                                write_date   

                                                                    FROM casos_legal')
                                                                                            AS t1(    id integer ,
                                                            datos_jornada_calendario varchar, 
                                                            estatus varchar,
                                                            cedula varchar, 
                                                            nombre varchar, 
                                                            apellido varchar, 
                                                            observaciones_caso text, 
                                                            tripulante_asignado integer, 
                                                            recaudos_recibidos varchar, 
                                                            fecha_documento_entregado date, 
                                                            datos_asesoria integer, 
                                                            descripcion_asesoria text, 
                                                            cedula_parte2 varchar, 
                                                            nombre_parte2 varchar, 
                                                            direccion_parte2 text, 
                                                            fecha_citacion date, 
                                                            categoria_area_legal varchar, 
                                                            create_uid integer, 
                                                            create_date timestamp, 
                                                            write_uid integer, 
                                                            write_date timestamp )
                                    RIGHT JOIN
                                            dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 'SELECT  id  ,
                                                                                    datos_jornada_calendario, 
                                                                                    estatus,
                                                                                    cedula, 
                                                                                    nombre, 
                                                                                    apellido, 
                                                                                    observaciones_caso, 
                                                                                    tripulante_asignado , 
                                                                                    recaudos_recibidos, 
                                                                                    fecha_documento_entregado, 
                                                                                    datos_asesoria , 
                                                                                    descripcion_asesoria, 
                                                                                    cedula_parte2, 
                                                                                    nombre_parte2, 
                                                                                    direccion_parte2, 
                                                                                    fecha_citacion, 
                                                                                    categoria_area_legal, 
                                                                                    create_uid , 
                                                                                    create_date, 
                                                                                    write_uid , 
                                                                                    write_date    

                                                                                FROM casos_legal')
                                                                            AS t2( id integer ,
                                                                                datos_jornada_calendario varchar, 
                                                                                estatus varchar,
                                                                                cedula varchar, 
                                                                                nombre varchar, 
                                                                                apellido varchar, 
                                                                                observaciones_caso text, 
                                                                                tripulante_asignado integer, 
                                                                                recaudos_recibidos varchar, 
                                                                                fecha_documento_entregado date, 
                                                                                datos_asesoria integer, 
                                                                                descripcion_asesoria text, 
                                                                                cedula_parte2 varchar, 
                                                                                nombre_parte2 varchar, 
                                                                                direccion_parte2 text, 
                                                                                fecha_citacion date, 
                                                                                categoria_area_legal varchar, 
                                                                                create_uid integer, 
                                                                                create_date timestamp, 
                                                                                write_uid integer, 
                                                                                write_date timestamp )
                                        ON T1.create_date = T2.create_date 
                                            AND T1.datos_jornada_calendario = T2.datos_jornada_calendario
                                            AND T1.cedula = T2.cedula
                                            AND T1.categoria_area_legal = T2.categoria_area_legal
                                            AND T1.estatus = T2.estatus
                        WHERE  T1.create_date IS NULL
                                            AND T1.datos_jornada_calendario IS NULL
                                            AND T1.cedula IS NULL
                                            AND T1.categoria_area_legal IS NULL
                                            AND T1.estatus = T2.estatus IS NULL
                                """
            cur.execute(sql)
            if cur.rowcount > 0:
                list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %(NOMBRE_TABLA))
                campo_actualizar = cur.fetchall()
                descripcion = cur.description
                
                for update_casos_legal in campo_actualizar:
                    i = 0
                    sql = ' UPDATE  %s SET ' % (NOMBRE_TABLA)
                    for cd in descripcion:
                        if update_casos_legal[i]:
                            # print(cd.name)
                            if len(update_casos_legal) -1 == i:
                                sql = sql + cd.name + '=\'%s\'' % (update_casos_legal[i])
                                
                            else:
                                sql = sql + cd.name + '=\'%s\',' % (update_casos_legal[i])
                        i=i+1
                    sql = sql + ' WHERE datos_jornada_calendario=\'%s\' AND   cedula=\'%s\' AND   categoria_area_legal=\'%s\' AND create_date=\'%s\'' % (update_casos_legal[0],
                                                                                                                                                        update_casos_legal[2],
                                                                                                                                                        update_casos_legal[15],
                                                                                                                                                        update_casos_legal[17])
                    cur.execute(sql)
                    if cur.rowcount > 0:
                        conexion.commit()
                        list_.append('Se actualizó el registro [CI: %s Nom: %s] de la tabla << %s >> en la PC local (%s)' %(update_casos_legal[2],update_casos_legal[3],NOMBRE_TABLA,cur.statusmessage))
                    else:
                        list_.append('No hubo actualización en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                #         self.ENTRAR_ACT_2 = False
                # list_.append('ENTRAR_ACT_2: %s' % (self.ENTRAR_ACT_2))
                list_.append('---------------------------------------------------------------------------------')

            else:
                list_.append('La consulta NO encontró diferencias entre la tabla << %s >> del Servidor y la PC local (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                self.ENTRAR_ACT_2 = False
                list_.append('ENTRAR_ACT_2: %s' % (self.ENTRAR_ACT_2))
        except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función action_actualizar_casos_legal_sin_campos_relacion' % (error, NOMBRE_TABLA))
        finally:
            cur.close()
            conexion.close()
    
    #2.3
    def action_actualizar_casos_legal(self):
        list_.append('Inicio de la función # 2.3 << action_actualizar_casos_legal >>')
        
        continuar_eje = True
        CONTINUAR_EJE_2 = True
        CONTINUAR_EJE_3 = 0
        NOMBRE_TABLA = 'public.casos_legal_instruccion_valor_rel_aux'

        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        USER_LOCAL="openpg"
        PASSWORD_LOCAL="openpgpwd"

        # HOST_SERVER="127.0.0.1"
        # DATABASE_SERVER="provene_local_6"
        # USER_SERVER="openpg"
        # PASSWORD_SERVER="openpgpwd"

        try:
            conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
            cur = conexion.cursor()
            sql = """ CREATE TABLE %s
                        (
                        A_id integer,
                        B_id integer 
                        )
                """ % (NOMBRE_TABLA)
            cur.execute(sql)
            conexion.commit()
            continuar_eje = True
            list_.append('Se creó la tabla temporal << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
            print(cur.statusmessage)    
                
        except (Exception, psycopg2.DatabaseError) as error:
            if error.pgcode != '42P07':
                continuar_eje = False
                list_.append('Error: %s. Al intentar crear la tabla temporal << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                print(error)
                   
        finally:
            cur.close()
            conexion.close()

        if continuar_eje:

            try:
                conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)
                cur = conexion.cursor()
                sql = 'DELETE FROM %s ' % (NOMBRE_TABLA)
                cur.execute(sql)
                conexion.commit()
                list_.append('Se limpió la información de la tabla temporal << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                print(cur.statusmessage)
            except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar limpiar la tabla << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                print(error)
            finally:
                cur.close()
                conexion.close()
            try:
                conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
                cur = conexion.cursor()
                sql = """ 	INSERT INTO %s
                                (A_id,B_id)
                            SELECT  T2.casos_legal_id, 
                                    T2.instruccion_valor_id							  
                            FROM  dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 
                                                                        'SELECT casos_legal_id,
                                                                            instruccion_valor_id 
                                                                        FROM casos_legal_instruccion_valor_rel')
                                                                            AS t1( casos_legal_id integer ,instruccion_valor_id integer)
                            RIGHT JOIN
                                dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 
                                                                            'SELECT casos_legal_id,
                                                                                        instruccion_valor_id
                                                                            FROM casos_legal_instruccion_valor_rel')
                                                                            AS t2(casos_legal_id integer ,instruccion_valor_id integer)
                            ON T1.casos_legal_id = T2.casos_legal_id
                                AND T1.instruccion_valor_id = T2.instruccion_valor_id
                            WHERE T1.casos_legal_id IS NULL 
                                AND T1.instruccion_valor_id IS NULL 
                    """ % (NOMBRE_TABLA)
                cur.execute(sql)
                if cur.rowcount > 0:
                    conexion.commit()
                    list_.append('Se insertó en la tabla temporal << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
                    CONTINUAR_EJE_2 = True
                else:
                    list_.append('No hubo inserciones en la tabla temporal << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                    CONTINUAR_EJE_2 = False
                print(cur.statusmessage)
            except (Exception, psycopg2.DatabaseError) as error:
                    list_.append('Error: %s. Al intentar insertar registros la tabla temporal << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                    print(error)
                    CONTINUAR_EJE_2 = False
            finally:
                cur.close()
                conexion.close()
        
            if CONTINUAR_EJE_2:
                # Actualizan los campos cuando en el Servidor hay un cambio, en caso contrario esta consulta es vacia
                try:
                    conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
                    cur = conexion.cursor()
                    sql = """ SELECT	T2.casos_legal_id, 
                                        T2.instruccion_valor_id,
                                        T1.id,
                                        T2.id, 
                                        T2.datos_jornada_calendario, 
                                        T2.estatus,
                                        T2.cedula, 
                                        T2.nombre, 
                                        T2.apellido, 
                                        T2.observaciones_caso, 
                                        T2.tripulante_asignado , 
                                        T2.recaudos_recibidos, 
                                        T2.fecha_documento_entregado, 
                                        T2.datos_asesoria , 
                                        T2.descripcion_asesoria, 
                                        T2.cedula_parte2, 
                                        T2.nombre_parte2, 
                                        T2.direccion_parte2, 
                                        T2.fecha_citacion, 
                                        T2.categoria_area_legal, 
                                        T2.create_uid , 
                                        T2.create_date, 
                                        T2.write_uid , 
                                        T2.write_date
                            FROM  	dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 'SELECT    id  ,
                                                        datos_jornada_calendario, 
                                                        estatus,
                                                        cedula, 
                                                        nombre, 
                                                        apellido, 
                                                        observaciones_caso, 
                                                        tripulante_asignado , 
                                                        recaudos_recibidos, 
                                                        fecha_documento_entregado, 
                                                        datos_asesoria , 
                                                        descripcion_asesoria, 
                                                        cedula_parte2, 
                                                        nombre_parte2, 
                                                        direccion_parte2, 
                                                        fecha_citacion, 
                                                        categoria_area_legal, 
                                                        create_uid , 
                                                        create_date, 
                                                        write_uid , 
                                                        write_date   

                                                            FROM casos_legal')
                                                                                    AS t1(    id integer ,
                                                    datos_jornada_calendario varchar, 
                                                    estatus varchar,
                                                    cedula varchar, 
                                                    nombre varchar, 
                                                    apellido varchar, 
                                                    observaciones_caso text, 
                                                    tripulante_asignado integer, 
                                                    recaudos_recibidos varchar, 
                                                    fecha_documento_entregado date, 
                                                    datos_asesoria integer, 
                                                    descripcion_asesoria text, 
                                                    cedula_parte2 varchar, 
                                                    nombre_parte2 varchar, 
                                                    direccion_parte2 text, 
                                                    fecha_citacion date, 
                                                    categoria_area_legal varchar, 
                                                    create_uid integer, 
                                                    create_date timestamp, 
                                                    write_uid integer, 
                                                    write_date timestamp )
                            INNER JOIN
                                    dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 'SELECT   	CLIV.casos_legal_id, 
                                                                            CLIV.instruccion_valor_id,
                                                                            id  ,
                                                                            datos_jornada_calendario, 
                                                                            estatus,
                                                                            cedula, 
                                                                            nombre, 
                                                                            apellido, 
                                                                            observaciones_caso, 
                                                                            tripulante_asignado , 
                                                                            recaudos_recibidos, 
                                                                            fecha_documento_entregado, 
                                                                            datos_asesoria , 
                                                                            descripcion_asesoria, 
                                                                            cedula_parte2, 
                                                                            nombre_parte2, 
                                                                            direccion_parte2, 
                                                                            fecha_citacion, 
                                                                            categoria_area_legal, 
                                                                            create_uid , 
                                                                            create_date, 
                                                                            write_uid , 
                                                                            write_date    

                                                                        FROM casos_legal CL, casos_legal_instruccion_valor_rel CLIV
                                                                        WHERE CL.ID = CLIV.casos_legal_id')
                                                                    AS t2(    casos_legal_id integer, 
                                                                        instruccion_valor_id integer,
                                                                        id integer ,
                                                                        datos_jornada_calendario varchar, 
                                                                        estatus varchar,
                                                                        cedula varchar, 
                                                                        nombre varchar, 
                                                                        apellido varchar, 
                                                                        observaciones_caso text, 
                                                                        tripulante_asignado integer, 
                                                                        recaudos_recibidos varchar, 
                                                                        fecha_documento_entregado date, 
                                                                        datos_asesoria integer, 
                                                                        descripcion_asesoria text, 
                                                                        cedula_parte2 varchar, 
                                                                        nombre_parte2 varchar, 
                                                                        direccion_parte2 text, 
                                                                        fecha_citacion date, 
                                                                        categoria_area_legal varchar, 
                                                                        create_uid integer, 
                                                                        create_date timestamp, 
                                                                        write_uid integer, 
                                                                        write_date timestamp )
                                ON T1.create_date = T2.create_date 
                                    AND T1.datos_jornada_calendario = T2.datos_jornada_calendario
                                    AND T1.cedula = T2.cedula
                                    AND T1.categoria_area_legal = T2.categoria_area_legal
                                    AND T1.estatus = T2.estatus
                                        """
                    cur.execute(sql)
                    if cur.rowcount > 0:
                        list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %('casos_legal'))
                        campo_actualizar = cur.fetchall()
                        descripcion = cur.description
                        CONTINUAR_EJE_3 = 0
                        
                        for update_casos_legal in campo_actualizar:
                            i = 0
                            sql = ' UPDATE  %s SET ' % (NOMBRE_TABLA)
                            for cd in descripcion:
                                if i == 0:
                                    # print(cd.name)
                                    sql = sql + 'A_id' + '=\'%s\'' % (update_casos_legal[2])
                                i=i+1
                            sql = sql + ' WHERE A_id=\'%s\' AND B_id=\'%s\'' % (update_casos_legal[0],update_casos_legal[1])
                            cur.execute(sql)
                            
                            if cur.rowcount > 0:
                                conexion.commit()
                                CONTINUAR_EJE_3 = CONTINUAR_EJE_3 + 1
                                list_.append('Se actualizó el registro [id: %s id: %s] de la tabla << %s >> en la PC local (%s)' %(update_casos_legal[0],update_casos_legal[1],NOMBRE_TABLA,cur.statusmessage))
                            else:
                                list_.append('No hubo actualización en la tabla << %s >> de la PC local  para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                        list_.append('---------------------------------------------------------------------------------')
                            # if cur.rowcount > 0:
                            #     conexion.commit()
                            #     CONTINUAR_EJE_3 = CONTINUAR_EJE_3 + 1
                            # print(cur.statusmessage)
                        
                    else:
                        list_.append('La consulta NO encontró diferencias entre la tabla << %s >> del Servidor y la PC local (%s)' %('casos_legal',cur.statusmessage))			
                        print(cur.statusmessage)
                except (Exception, psycopg2.DatabaseError) as error:
                        list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                        print(error)
                finally:
                    cur.close()
                    conexion.close()
                if CONTINUAR_EJE_3 > 0:
                    try:
                        conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)
                        cur = conexion.cursor()
                        sql = """ 	INSERT INTO casos_legal_instruccion_valor_rel
                                    SELECT  T2.casos_legal_id, T2.instruccion_valor_id
                                    FROM    dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 'SELECT casos_legal_id,
                                                                                                instruccion_valor_id
                                                                                    FROM casos_legal_instruccion_valor_rel')
                                                                                    AS t1(casos_legal_id integer ,instruccion_valor_id integer)
                                    RIGHT JOIN
                                            dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 'SELECT A_id,
                                                                                    B_id 
                                                                                FROM %s')
                                                                                    AS t2( casos_legal_id integer ,instruccion_valor_id integer)
                                        
                                    ON T1.casos_legal_id = T2.casos_legal_id
                                        AND T1.instruccion_valor_id = T2.instruccion_valor_id
                                    WHERE T1.casos_legal_id IS NULL 
                                          AND T1.casos_legal_id IS NULL """ % (NOMBRE_TABLA)
                        cur.execute(sql)
                        if cur.rowcount > 0:
                            conexion.commit()
                            list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %('casos_legal_instruccion_valor_rel',cur.statusmessage))
                        else:
                            list_.append('No hubo inserciones en la tabla << %s >> de la PC local para este caso (%s)' %('casos_legal_instruccion_valor_rel',cur.statusmessage))
                        print(cur.statusmessage)
                            
                    except (Exception, psycopg2.DatabaseError) as error:
                        print(error)
                        list_.append('Error: (%s). Al intentar insertar en la tabla << %s >> en la función action_bajar_casos_legal' %(error, 'casos_legal_instruccion_valor_rel'))
                        _logger.info('Casos Legales action_actualizar_casos_legal........................................................................... 3 %s' % (error))
              
                    finally:
                        cur.close()
                        conexion.close()
                else:
                    list_.append("No habían datos en <<%s>> que actualizar" % (NOMBRE_TABLA))
            else:
                list_.append("No se puede continuar la TABLA <<casos_legal_instruccion_valor_rel>> ¡ESTÁ VACÍA!")
            try:
                conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
                cur = conexion.cursor()
                sql = 'DROP TABLE %s ' % (NOMBRE_TABLA)
                cur.execute(sql)
                conexion.commit()
                # continuar_eje = True
                list_.append('Se Eliminó la tabla temporal << %s >> en la PC local con éxito (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                print(cur.statusmessage)   
                    
            except (Exception, psycopg2.DatabaseError) as error:
                list_.append('Error: %s. Al intentar eliminar la tabla temporal << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                print(error)
            finally:
                cur.close()
                conexion.close()
        else:
            print("No se pudo continuar ejecutando esta función porque la TABLA PIVOTE <<casos_legal_instruccion_valor_rel_aux>> generó un error ")        
    
    #2.4
    def action_actualizar_casos_legal_tripulante_asignado(self):
        list_.append('Inicio de la función # 2.4 << action_actualizar_casos_legal_tripulante_asignado >>')
        
        NOMBRE_TABLA = 'public.casos_legal'

        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        USER_LOCAL="openpg"
        PASSWORD_LOCAL="openpgpwd"
        try:
            # if self.resultados_actualizar == False or self.resultados_actualizar == '':
            #     self.resultados_actualizar = ' '
            conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
            cur = conexion.cursor()
            sql = """  	SELECT t2.tripulante_asignado, t1.id, t2.datos_jornada_calendario, t2.create_date
                        FROM  	dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 
                                    'SELECT  	id  ,
                                                login
                                    FROM res_users') AS t1( id integer ,
                                                            login varchar)
                        INNER JOIN
                                dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 
                                    'SELECT 	ru.login,
                                                cl.id  ,
                                                datos_jornada_calendario, 
                                                estatus,
                                                cedula, 
                                                nombre, 
                                                apellido, 
                                                observaciones_caso, 
                                                tripulante_asignado , 
                                                recaudos_recibidos, 
                                                fecha_documento_entregado, 
                                                datos_asesoria , 
                                                descripcion_asesoria, 
                                                cedula_parte2, 
                                                nombre_parte2, 
                                                direccion_parte2, 
                                                fecha_citacion, 
                                                categoria_area_legal, 
                                                cl.create_uid , 
                                                cl.create_date, 
                                                cl.write_uid , 
                                                cl.write_date    

                                        FROM res_users ru,casos_legal cl
                                        WHERE  ru.id = cl.tripulante_asignado') AS t2(  login varchar,
                                                                                        id integer ,
                                                                                        datos_jornada_calendario varchar, 
                                                                                        estatus varchar,
                                                                                        cedula varchar, 
                                                                                        nombre varchar, 
                                                                                        apellido varchar, 
                                                                                        observaciones_caso text, 
                                                                                        tripulante_asignado integer, 
                                                                                        recaudos_recibidos varchar, 
                                                                                        fecha_documento_entregado date, 
                                                                                        datos_asesoria integer, 
                                                                                        descripcion_asesoria text, 
                                                                                        cedula_parte2 varchar, 
                                                                                        nombre_parte2 varchar, 
                                                                                        direccion_parte2 text, 
                                                                                        fecha_citacion date, 
                                                                                        categoria_area_legal varchar, 
                                                                                        create_uid integer, 
                                                                                        create_date timestamp, 
                                                                                        write_uid integer, 
                                                                                        write_date timestamp )
                        ON T1.login = T2.login
                                """
            cur.execute(sql)
            if cur.rowcount > 0:
                list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %(NOMBRE_TABLA))
                campo_actualizar = cur.fetchall()
                descripcion = cur.description
                
                for update_casos_legal in campo_actualizar:
                    i = 0
                    sql = ' UPDATE  %s SET ' % (NOMBRE_TABLA)
                    for cd in descripcion:
                        if i == 0:
                            # print(cd.name)
                            sql = sql + cd.name + '=\'%s\'' % (update_casos_legal[1])
                        i=i+1
                    sql = sql + ' WHERE tripulante_asignado=\'%s\' AND datos_jornada_calendario=\'%s\' AND create_date=\'%s\' ' % (	update_casos_legal[0],
                                                                                                                                    update_casos_legal[2],
                                                                                                                                    update_casos_legal[3])
                    cur.execute(sql)
                    if cur.rowcount > 0:
                        conexion.commit()
                        list_.append('Se actualizó el registro [Trip. Asig.: %s Datos Jornada: %s] de la tabla << %s >> en la PC local (%s)' %(update_casos_legal[0],update_casos_legal[2],NOMBRE_TABLA,cur.statusmessage))
                    else:
                        list_.append('No hubo actualización en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                list_.append('---------------------------------------------------------------------------------')
                    # if cur.rowcount > 0:
                    #     conexion.commit()
                        
                    # self.resultados_actualizar = str('Tripulante Asignado de Casos Legales Actualizadas con Éxito' + '\n ' + self.resultados_actualizar)
                    # _logger.info('Casos Legales........................................................................... 1 %s' % (cur.statusmessage))
            else:
                list_.append('La consulta NO encontró diferencias entre la tabla << %s >> del Servidor y la PC local (%s)' %(NOMBRE_TABLA,cur.statusmessage))			
                # self.resultados_actualizar = str(cur.statusmessage + '\n ' + self.resultados_actualizar)
                _logger.info('........................................................................... 2 %s' % (cur.statusmessage))
                
        except (Exception, psycopg2.DatabaseError) as error:
            # self.resultados_actualizar = str(error + '\n ' + self.resultados_actualizar)
            list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función action_actualizar_casos_legal_tripulante_asignado' % (error, NOMBRE_TABLA))
            _logger.info('........................................................................... 3 %s' % (error))
                
        finally:
            cur.close()
            conexion.close()
              
    #2.5 
    def action_actualizar_casos_legal_write_uid(self):
        list_.append('Inicio de la función # 2.5 << action_actualizar_casos_legal_write_uid >>')
        
        NOMBRE_TABLA = 'public.casos_legal'

        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        USER_LOCAL="openpg"
        PASSWORD_LOCAL="openpgpwd"
        try:
            conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
            cur = conexion.cursor()
            sql = """  	SELECT t2.write_uid, t1.id, t2.datos_jornada_calendario, t2.create_date
                        FROM  	dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 
                                    'SELECT  	id  ,
                                                login
                                    FROM res_users') AS t1( id integer ,
                                                            login varchar)
                        INNER JOIN
                                dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 
                                    'SELECT 	ru.login,
                                                cl.id  ,
                                                datos_jornada_calendario, 
                                                estatus,
                                                cedula, 
                                                nombre, 
                                                apellido, 
                                                observaciones_caso, 
                                                tripulante_asignado , 
                                                recaudos_recibidos, 
                                                fecha_documento_entregado, 
                                                datos_asesoria , 
                                                descripcion_asesoria, 
                                                cedula_parte2, 
                                                nombre_parte2, 
                                                direccion_parte2, 
                                                fecha_citacion, 
                                                categoria_area_legal, 
                                                cl.create_uid , 
                                                cl.create_date, 
                                                cl.write_uid , 
                                                cl.write_date    

                                        FROM res_users ru,casos_legal cl
                                        WHERE  ru.id = cl.write_uid') AS t2(  login varchar,
                                                                                        id integer ,
                                                                                        datos_jornada_calendario varchar, 
                                                                                        estatus varchar,
                                                                                        cedula varchar, 
                                                                                        nombre varchar, 
                                                                                        apellido varchar, 
                                                                                        observaciones_caso text, 
                                                                                        tripulante_asignado integer, 
                                                                                        recaudos_recibidos varchar, 
                                                                                        fecha_documento_entregado date, 
                                                                                        datos_asesoria integer, 
                                                                                        descripcion_asesoria text, 
                                                                                        cedula_parte2 varchar, 
                                                                                        nombre_parte2 varchar, 
                                                                                        direccion_parte2 text, 
                                                                                        fecha_citacion date, 
                                                                                        categoria_area_legal varchar, 
                                                                                        create_uid integer, 
                                                                                        create_date timestamp, 
                                                                                        write_uid integer, 
                                                                                        write_date timestamp )
                        ON T1.login = T2.login
                                """
            cur.execute(sql)
            if cur.rowcount > 0:
                list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %(NOMBRE_TABLA))
                campo_actualizar = cur.fetchall()
                descripcion = cur.description
                
                for update_casos_legal in campo_actualizar:
                    i = 0
                    sql = ' UPDATE  %s SET ' % (NOMBRE_TABLA)
                    for cd in descripcion:
                        if i == 0:
                            # print(cd.name)
                            sql = sql + cd.name + '=\'%s\'' % (update_casos_legal[1])
                        i=i+1
                    sql = sql + ' WHERE datos_jornada_calendario=\'%s\' AND create_date=\'%s\' ' % (update_casos_legal[2],	update_casos_legal[3])
                    cur.execute(sql)
                    if cur.rowcount > 0:
                        conexion.commit()
                        list_.append('Se actualizó el registro [Write id.: %s Datos Jornada: %s] de la tabla << %s >> en la PC local (%s)' %(update_casos_legal[1],update_casos_legal[2],NOMBRE_TABLA,cur.statusmessage))
                    else:
                        list_.append('No hubo actualización en la tabla << %s >> de la PC local para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                list_.append('---------------------------------------------------------------------------------')
            else:
                list_.append('La consulta NO encontró diferencias entre la tabla << %s >> del Servidor y la PC local (%s)' %(NOMBRE_TABLA,cur.statusmessage))			
                _logger.info('........................................................................... 2 %s' % (cur.statusmessage))
                
        except (Exception, psycopg2.DatabaseError) as error:
            list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función action_actualizar_casos_legal_write_uid' % (error, NOMBRE_TABLA))
            _logger.info('........................................................................... 3 %s' % (error))
                
        finally:
            cur.close()
            conexion.close()
            
        # self.mostrar_resultados_update()
  
    #2
    def action_actualizar_casos_legal_completamente(self):
      
        try:
            self.ENTRAR_ACT_1 = True
            self.ENTRAR_ACT_2 = True
            
            # 2.1
            self.action_bajar_casos_legal_create_y_write_uid()
            list_.append('Salió de la función << action_bajar_casos_legal_create_y_write_uid >>')
            
            # 2.2
            self.action_actualizar_casos_legal_sin_campos_relacion()
            list_.append('Salió de la función << action_actualizar_casos_legal_sin_campos_relacion >>')
            
            if self.ENTRAR_ACT_1 or self.ENTRAR_ACT_2:
                # 2.3
                self.action_actualizar_casos_legal()
                list_.append('Salió de la función << action_actualizar_casos_legal >>')
                
                # 2.4
                self.action_actualizar_casos_legal_tripulante_asignado()
                list_.append('Salió de la función << action_actualizar_casos_legal_tripulante_asignado >>')
                
                # 2.5
                self.action_actualizar_casos_legal_write_uid()
                list_.append('Salió de la función << action_actualizar_casos_legal_write_uid >>')

            # 0.1
            self.mostrar_resultados_update()
            
            # self.resultados_actualizar = str('Casos Legales Actualizadas con Éxito por completo' + '\n ' + self.resultados_actualizar)
        
        except (Exception, psycopg2.DatabaseError) as error:
            list_.append('Error: %s. al intentar actualizar la tabla << casos_legal >> por COMPLETO del PC Local' %(error))
            _logger.info('........................................................................... 3 action_actualizar_casos_legal_completamente %s' % (error))
            self.mostrar_resultados_update()

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

    #1.1 Prueba de registro asesoria nuevo No funciona correctamente
    def action_bajar_registro_asesoria_(self): 
        
        NOMBRE_TABLA = 'public.registro_asesoria'
        # NOMBRE_TABLA_REAL = 'public.registro_asesoria_registro_cuestionario1_c21_rel'
        NOMBRE_FUNCION = 'action_bajar_registro_asesoria_'
        list_.append('Inicio de la función # Prueba << %s >>' % (NOMBRE_FUNCION))

        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        USER_LOCAL="openpg"
        PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
            cur = conexion.cursor()
            # cur2 = conexion.cursor()
            # cr = self.env.cr
            sql = """  		SELECT RU.id, 
																		T3.login,
																		T3.id ,
												T3.datos_jornada_calendario,
												T3.nombre,
												T3.apellido,
												T3.foto_carnet_clave,
												T3.nacionalidad_real,
												T3.cedula,
												T3.fecha_nacimiento,
												T3.email,
												T3.genero,
												T3.estado_civil,
												T3.nacionalidad ,
												T3.estado ,
												T3.municipio ,
												T3.parroquia ,
												T3.calle_callejon_av_trs,
												T3.casa_edif,
												T3.escalera,
												T3.piso,
												T3.apartamento,
												T3.barrio_urb_zona,
												T3.direccion,
												T3.telefono_habitacion,
												T3.telefono_celular,
												T3.telefono_trabajo,
												T3.hora_contacto,
												T3.c4_nexo_familiar,
												T3.c5_grado_instruccion,
												T3.c6_situacion_ocupacion,
												T3.c7_tipo_vivienda,
												T3.c8_tenencia_vivienda,
												T3.c9_personas_viven_usted ,
												T3.c10_personas_menores_6 ,
												T3.c11_personas_menores_6_12 ,
												T3.c12_personas_menores_6_12_escuela,
												T3.c13_frecuencia_escuela,
												T3.c14_personas_ingresos ,
												T3.c15_ingreso_hogar,
												T3.c16_principal_hogar,
												T3.c17_familia_exterior,
												T3.c18_ayuda_economica_exterior,
												T3.c20_comidas_diarias,
												T3.c22_referido,
												T3.cl1_servicio,
												T3.cl2_canalizar,
												T3.cl3_solicitar,
												T3.cl4_asistencia,
												T3.cl5_tramite,
												T3.cl6_tribunales,
												T3.cl7_experiencia,
												T3.cl8_ddhh,
												T3.cl9_justicia,
												T3.cl10_transicional,
												T3.cs1_actividad,
												T3.cs3_capacidad,
												T3.cs5_contribuir,
												T3.cs7_participar_actividades,
												T3.cs8_ayuda_economica_exterior,
												T3.create_uid ,
												T3.create_date ,
												T3.write_uid ,
												T3.write_date 
																		FROM (
																		SELECT	T2.login,
																		T2.id ,
								T2.datos_jornada_calendario,
								T2.nombre,
								T2.apellido,
								T2.foto_carnet_clave,
								T2.nacionalidad_real,
								T2.cedula,
								T2.fecha_nacimiento,
								T2.email,
								T2.genero,
								T2.estado_civil,
								T2.nacionalidad ,
								T2.estado ,
								T2.municipio ,
								T2.parroquia ,
								T2.calle_callejon_av_trs,
								T2.casa_edif,
								T2.escalera,
								T2.piso,
								T2.apartamento,
								T2.barrio_urb_zona,
								T2.direccion,
								T2.telefono_habitacion,
								T2.telefono_celular,
								T2.telefono_trabajo,
								T2.hora_contacto,
								T2.c4_nexo_familiar,
								T2.c5_grado_instruccion,
								T2.c6_situacion_ocupacion,
								T2.c7_tipo_vivienda,
								T2.c8_tenencia_vivienda,
								T2.c9_personas_viven_usted ,
								T2.c10_personas_menores_6 ,
								T2.c11_personas_menores_6_12 ,
								T2.c12_personas_menores_6_12_escuela,
								T2.c13_frecuencia_escuela,
								T2.c14_personas_ingresos ,
								T2.c15_ingreso_hogar,
								T2.c16_principal_hogar,
								T2.c17_familia_exterior,
								T2.c18_ayuda_economica_exterior,
								T2.c20_comidas_diarias,
								T2.c22_referido,
								T2.cl1_servicio,
								T2.cl2_canalizar,
								T2.cl3_solicitar,
								T2.cl4_asistencia,
								T2.cl5_tramite,
								T2.cl6_tribunales,
								T2.cl7_experiencia,
								T2.cl8_ddhh,
								T2.cl9_justicia,
								T2.cl10_transicional,
								T2.cs1_actividad,
								T2.cs3_capacidad,
								T2.cs5_contribuir,
								T2.cs7_participar_actividades,
								T2.cs8_ayuda_economica_exterior,
								T2.create_uid ,
								T2.create_date ,
								T2.write_uid ,
								T2.write_date 
															FROM  dblink(   'host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 
																														'SELECT id ,
								datos_jornada_calendario,
								nombre,
								apellido,
								foto_carnet_clave,
								nacionalidad_real,
								cedula,
								fecha_nacimiento,
								email,
								genero,
								estado_civil,
								nacionalidad ,
								estado ,
								municipio ,
								parroquia ,
								calle_callejon_av_trs,
								casa_edif,
								escalera,
								piso,
								apartamento,
								barrio_urb_zona,
								direccion,
								telefono_habitacion,
								telefono_celular,
								telefono_trabajo,
								hora_contacto,
								c4_nexo_familiar,
								c5_grado_instruccion,
								c6_situacion_ocupacion,
								c7_tipo_vivienda,
								c8_tenencia_vivienda,
								c9_personas_viven_usted ,
								c10_personas_menores_6 ,
								c11_personas_menores_6_12 ,
								c12_personas_menores_6_12_escuela,
								c13_frecuencia_escuela,
								c14_personas_ingresos ,
								c15_ingreso_hogar,
								c16_principal_hogar,
								c17_familia_exterior,
								c18_ayuda_economica_exterior,
								c20_comidas_diarias,
								c22_referido,
								cl1_servicio,
								cl2_canalizar,
								cl3_solicitar,
								cl4_asistencia,
								cl5_tramite,
								cl6_tribunales,
								cl7_experiencia,
								cl8_ddhh,
								cl9_justicia,
								cl10_transicional,
								cs1_actividad,
								cs3_capacidad,
								cs5_contribuir,
								cs7_participar_actividades,
								cs8_ayuda_economica_exterior,
								create_uid ,
								create_date ,
								write_uid ,
								write_date 
																																FROM registro_asesoria')  AS t1(id integer,
								datos_jornada_calendario character varying,
								nombre character varying,
								apellido character varying,
								foto_carnet_clave text,
								nacionalidad_real character varying,
								cedula character varying,
								fecha_nacimiento date,
								email character varying,
								genero character varying,
								estado_civil character varying,
								nacionalidad integer,
								estado integer,
								municipio integer,
								parroquia integer,
								calle_callejon_av_trs character varying,
								casa_edif character varying,
								escalera character varying,
								piso character varying,
								apartamento character varying,
								barrio_urb_zona character varying,
								direccion text,
								telefono_habitacion character varying,
								telefono_celular character varying,
								telefono_trabajo character varying,
								hora_contacto character varying,
								c4_nexo_familiar character varying,
								c5_grado_instruccion character varying,
								c6_situacion_ocupacion character varying,
								c7_tipo_vivienda character varying,
								c8_tenencia_vivienda character varying,
								c9_personas_viven_usted integer,
								c10_personas_menores_6 integer,
								c11_personas_menores_6_12 integer,
								c12_personas_menores_6_12_escuela character varying,
								c13_frecuencia_escuela character varying,
								c14_personas_ingresos integer,
								c15_ingreso_hogar character varying,
								c16_principal_hogar character varying,
								c17_familia_exterior character varying,
								c18_ayuda_economica_exterior character varying,
								c20_comidas_diarias character varying,
								c22_referido character varying,
								cl1_servicio character varying,
								cl2_canalizar character varying,
								cl3_solicitar character varying,
								cl4_asistencia character varying,
								cl5_tramite character varying,
								cl6_tribunales character varying,
								cl7_experiencia character varying,
								cl8_ddhh character varying,
								cl9_justicia character varying,
								cl10_transicional character varying,
								cs1_actividad character varying,
								cs3_capacidad character varying,
								cs5_contribuir character varying,
								cs7_participar_actividades character varying,
								cs8_ayuda_economica_exterior text,
								create_uid integer,
								create_date timestamp,
								write_uid integer,
								write_date timestamp )
																								RIGHT JOIN 
									dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 
																														'SELECT   RU.login, 
																										CL.id  ,
								datos_jornada_calendario,
								nombre,
								apellido,
								foto_carnet_clave,
								nacionalidad_real,
								cedula,
								fecha_nacimiento,
								email,
								genero,
								estado_civil,
								nacionalidad ,
								estado ,
								municipio ,
								parroquia ,
								calle_callejon_av_trs,
								casa_edif,
								escalera,
								piso,
								apartamento,
								barrio_urb_zona,
								direccion,
								telefono_habitacion,
								telefono_celular,
								telefono_trabajo,
								hora_contacto,
								c4_nexo_familiar,
								c5_grado_instruccion,
								c6_situacion_ocupacion,
								c7_tipo_vivienda,
								c8_tenencia_vivienda,
								c9_personas_viven_usted ,
								c10_personas_menores_6 ,
								c11_personas_menores_6_12 ,
								c12_personas_menores_6_12_escuela,
								c13_frecuencia_escuela,
								c14_personas_ingresos ,
								c15_ingreso_hogar,
								c16_principal_hogar,
								c17_familia_exterior,
								c18_ayuda_economica_exterior,
								c20_comidas_diarias,
								c22_referido,
								cl1_servicio,
								cl2_canalizar,
								cl3_solicitar,
								cl4_asistencia,
								cl5_tramite,
								cl6_tribunales,
								cl7_experiencia,
								cl8_ddhh,
								cl9_justicia,
								cl10_transicional,
								cs1_actividad,
								cs3_capacidad,
								cs5_contribuir,
								cs7_participar_actividades,
								cs8_ayuda_economica_exterior,
                                                                                                    CL.create_uid , 
                                                                                                    CL.create_date, 
                                                                                                    CL.write_uid , 
                                                                                                    CL.write_date    
                                                                                            FROM registro_asesoria CL, res_users RU
                                                                                            WHERE CL.create_uid = RU.id')  AS t2(login character varying,
											id integer,
											datos_jornada_calendario character varying,
											nombre character varying,
											apellido character varying,
											foto_carnet_clave text,
											nacionalidad_real character varying,
											cedula character varying,
											fecha_nacimiento date,
											email character varying,
											genero character varying,
											estado_civil character varying,
											nacionalidad integer,
											estado integer,
											municipio integer,
											parroquia integer,
											calle_callejon_av_trs character varying,
											casa_edif character varying,
											escalera character varying,
											piso character varying,
											apartamento character varying,
											barrio_urb_zona character varying,
											direccion text,
											telefono_habitacion character varying,
											telefono_celular character varying,
											telefono_trabajo character varying,
											hora_contacto character varying,
											c4_nexo_familiar character varying,
											c5_grado_instruccion character varying,
											c6_situacion_ocupacion character varying,
											c7_tipo_vivienda character varying,
											c8_tenencia_vivienda character varying,
											c9_personas_viven_usted integer,
											c10_personas_menores_6 integer,
											c11_personas_menores_6_12 integer,
											c12_personas_menores_6_12_escuela character varying,
											c13_frecuencia_escuela character varying,
											c14_personas_ingresos integer,
											c15_ingreso_hogar character varying,
											c16_principal_hogar character varying,
											c17_familia_exterior character varying,
											c18_ayuda_economica_exterior character varying,
											c20_comidas_diarias character varying,
											c22_referido character varying,
											cl1_servicio character varying,
											cl2_canalizar character varying,
											cl3_solicitar character varying,
											cl4_asistencia character varying,
											cl5_tramite character varying,
											cl6_tribunales character varying,
											cl7_experiencia character varying,
											cl8_ddhh character varying,
											cl9_justicia character varying,
											cl10_transicional character varying,
											cs1_actividad character varying,
											cs3_capacidad character varying,
											cs5_contribuir character varying,
											cs7_participar_actividades character varying,
											cs8_ayuda_economica_exterior text,
											create_uid integer,
											create_date timestamp,
											write_uid integer,
											write_date timestamp )
																								ON T1.create_date = T2.create_date
                                                    WHERE T1.create_date IS NULL) T3, res_users RU
                            WHERE T3.LOGIN = RU.LOGIN

                                """ 
            cur.execute(sql)
            if cur.rowcount > 0:
                list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %(NOMBRE_TABLA))

                registro_asesorias = cur.fetchall()
                descripcion = cur.description
                values = []
                for registro_asesoria in registro_asesorias:
                    sql =   """ SELECT * 
                                FROM dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd',
                                            'SELECT cedula 
                                            FROM cedulas_venezuela_2012 
                                            WHERE cedula = %s ') as t1(A integer)
                            """ % (registro_asesoria[8])
                    cur.execute(sql)
                    # cr.execute(sql)
                    if cur.rowcount > 0:
                        cedula_existe_b = True
                    else:
                        cedula_existe_b = False
                        list_.append('Esta cédula [CI: %s Nom.: %s] se agregará en la tabla del cedulas_venezuela_2012 (%s)' %(registro_asesoria[8],registro_asesoria[4],cur.statusmessage))
                    
                    sql = """ 	SELECT *
                                FROM dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC',' 
                                select rac2.registro_cs2_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS2'' AS PREGUNTA, RA.NOMBRE
                                from registro_cs2 c2,registro_asesoria_registro_cs2_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cs2_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                UNION
                                select rac2.registro_cs4_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS4'' AS PREGUNTA, RA.NOMBRE
                                from registro_cs4 c2,registro_asesoria_registro_cs4_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cs4_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                UNION
                                select rac2.registro_cs6_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS6'' AS PREGUNTA, RA.NOMBRE
                                from registro_cs6 c2,registro_asesoria_registro_cs6_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cs6_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                UNION
                                select rac2.registro_cs9_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS9'' AS PREGUNTA, RA.NOMBRE
                                from registro_cs9 c2,registro_asesoria_registro_cs9_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cs9_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                UNION
                                select rac2.registro_cuestionario1_c19_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS19'' AS PREGUNTA, RA.NOMBRE
                                from registro_cuestionario1_c19 c2,registro_asesoria_registro_cuestionario1_c19_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cuestionario1_c19_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                UNION
                                select rac2.registro_cuestionario1_c21_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS21'' AS PREGUNTA, RA.NOMBRE
                                from registro_cuestionario1_c21 c2,registro_asesoria_registro_cuestionario1_c21_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cuestionario1_c21_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                ORDER BY PREGUNTA,REGISTRO_ASESORIA') AS T1 (A integer, B integer, C character varying, D character varying)
                                    """ % (	registro_asesoria[8],registro_asesoria[8],
                                            registro_asesoria[8],registro_asesoria[8],
                                            registro_asesoria[8],registro_asesoria[8])
                    # cur2.execute(sql)
                    cur.execute(sql)
                    if cur.rowcount > 0:
                        # if cur2.rowcount > 0:
                        registros = cur.fetchall()
                        # registros = cur2.fetchall()
                        CS2  = []
                        CS4  = []
                        CS6  = []
                        CS9  = []
                        CS19 = []
                        CS21 = []
                        for registro in registros:
                            if registro[2] == 'CS2':
                                CS2.append(registro[0])
                            if registro[2] == 'CS4':
                                CS4.append(registro[0])
                            if registro[2] == 'CS6':
                                CS6.append(registro[0])
                            if registro[2] == 'CS9':
                                CS9.append(registro[0])
                            if registro[2] == 'CS19':
                                CS19.append(registro[0])
                            if registro[2] == 'CS21':
                                CS21.append(registro[0])

                    values.append({
                        # 'id ':registro_asesoria[2],
                        'datos_jornada_calendario':registro_asesoria[3],
                        'nombre':registro_asesoria[4],
                        'apellido':registro_asesoria[5],
                        'foto_carnet_clave':registro_asesoria[6],
                        'nacionalidad_real':registro_asesoria[7],
                        'cedula':registro_asesoria[8],
                        'fecha_nacimiento':registro_asesoria[9],
                        'email':registro_asesoria[10],
                        'genero':registro_asesoria[11],
                        'estado_civil':registro_asesoria[12],
                        'nacionalidad':registro_asesoria[13],
                        'estado':registro_asesoria[14],
                        'municipio':registro_asesoria[15],
                        'parroquia':registro_asesoria[16],
                        'calle_callejon_av_trs':registro_asesoria[17],
                        'casa_edif':registro_asesoria[18],
                        'escalera':registro_asesoria[19],
                        'piso':registro_asesoria[20],
                        'apartamento':registro_asesoria[21],
                        'barrio_urb_zona':registro_asesoria[22],
                        'direccion':registro_asesoria[23],
                        'telefono_habitacion':registro_asesoria[24],
                        'telefono_celular':registro_asesoria[25],
                        'telefono_trabajo':registro_asesoria[26],
                        'hora_contacto':registro_asesoria[27],
                        'c4_nexo_familiar':registro_asesoria[28],
                        'c5_grado_instruccion':registro_asesoria[29],
                        'c6_situacion_ocupacion':registro_asesoria[30],
                        'c7_tipo_vivienda':registro_asesoria[31],
                        'c8_tenencia_vivienda':registro_asesoria[32],
                        'c9_personas_viven_usted':registro_asesoria[33],
                        'c10_personas_menores_6':registro_asesoria[34],
                        'c11_personas_menores_6_12':registro_asesoria[35],
                        'c12_personas_menores_6_12_escuela':registro_asesoria[36],
                        'c13_frecuencia_escuela':registro_asesoria[37],
                        'c14_personas_ingresos':registro_asesoria[38],
                        'c15_ingreso_hogar':registro_asesoria[39],
                        'c16_principal_hogar':registro_asesoria[40],
                        'c17_familia_exterior':registro_asesoria[41],
                        'c18_ayuda_economica_exterior':registro_asesoria[42],
                        'c20_comidas_diarias':registro_asesoria[43],
                        'c22_referido':registro_asesoria[44],
                        'cl1_servicio':registro_asesoria[45],
                        'cl2_canalizar':registro_asesoria[46],
                        'cl3_solicitar':registro_asesoria[47],
                        'cl4_asistencia':registro_asesoria[48],
                        'cl5_tramite':registro_asesoria[49],
                        'cl6_tribunales':registro_asesoria[50],
                        'cl7_experiencia':registro_asesoria[51],
                        'cl8_ddhh':registro_asesoria[52],
                        'cl9_justicia':registro_asesoria[53],
                        'cl10_transicional':registro_asesoria[54],
                        'cs1_actividad':registro_asesoria[55],
                        'cs3_capacidad':registro_asesoria[56],
                        'cs5_contribuir':registro_asesoria[57],
                        'cs7_participar_actividades':registro_asesoria[58],
                        'cs8_ayuda_economica_exterior':registro_asesoria[59],
                        'create_uid':registro_asesoria[60],
                        'create_date':registro_asesoria[61],
                        'write_uid':registro_asesoria[62],
                        'write_date':registro_asesoria[63],
                        'c19_beneficios_estado': [[6, False, CS19]],
                        'c21_principal_problema': [[6, False, CS21]],
                        'cs2_actividad_asistencia': [[6, False, CS2]],
                        'cs4_tribunales': [[6, False, CS4]],
                        'cs6_no_contribuir': [[6, False, CS6]],
                        'cs9_expectativas': [[6, False, CS9]],
                        'cedula_existe': cedula_existe_b,
				    })
                list_.append('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t %s' % (values, cur.statusmessage))
                _logger.info('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t %s' % (values, cur.statusmessage))

                record = self.env['registro.asesoria'].create(values)
                list_.append('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t' % (record))
                _logger.info('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t ' % (record))
                list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
                
                try:
                    list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %('registro_asesoria'))
                    
                    for registro_asesoria in registro_asesorias:

                        sql = ' UPDATE  %s SET ' % (NOMBRE_TABLA)
                        sql = sql + 'create_uid=\'%s\', create_date=\'%s\', write_date=\'%s\'' % (registro_asesoria[0],
                                                                                                    registro_asesoria[61],
                                                                                                    registro_asesoria[63])
                        
                        sql = sql + ' WHERE cedula=\'%s\' AND datos_jornada_calendario=\'%s\' '  % (registro_asesoria[8],
                                                                                                    registro_asesoria[3])
                        
                        list_.append('........................................................................... 100 \t\t\t\t %s \t\t\t\t ' % (sql))
                        _logger.info('........................................................................... 100 \t\t\t\t %s \t\t\t\t ' % (sql))
                        cur.execute(sql)
                        # cr.execute(sql)
                        
                        if cur.rowcount > 0:
                        # if cr.rowcount > 0:
                            conexion.commit()
                            list_.append('Se actualizó el registro [CI: %s Nom.: %s] de la tabla << %s >> en la PC local (%s)' %(registro_asesoria[7],registro_asesoria[4],NOMBRE_TABLA,cur.statusmessage))
                        else:
                            list_.append('No hubo actualización en la tabla << %s >> de la PC local  para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                    list_.append('------------------------------------------------------------------------------------------------------------')
                    self.action_actualizar_registro_asesoria_write_uid()
                except (Exception, psycopg2.DatabaseError) as error:
                        list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                        _logger.info('....................................................................................................3 %s' % (error))
                
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
        
        # mostrar_resultados_update()
    
    #1.2 Prueba de registro asesoria nuevo 2 No funciona correctamente
    def action_bajar_registro_asesoria_2(self):
        
        NOMBRE_TABLA = 'public.registro_asesoria'
        # NOMBRE_TABLA_REAL = 'public.registro_asesoria_registro_cuestionario1_c21_rel'
        NOMBRE_FUNCION = 'action_bajar_registro_asesoria_2'
        list_.append('Inicio de la función # Prueba 2 << %s >>' % (NOMBRE_FUNCION))

        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        USER_LOCAL="openpg"
        PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
            cur = conexion.cursor()
            # cur2 = conexion.cursor()
            # cr = self.env.cr
            sql = """  		SELECT RU.id, 
																		T3.login,
																		T3.id ,
												T3.datos_jornada_calendario,
												T3.nombre,
												T3.apellido,
												T3.foto_carnet_clave,
												T3.nacionalidad_real,
												T3.cedula,
												T3.fecha_nacimiento,
												T3.email,
												T3.genero,
												T3.estado_civil,
												T3.nacionalidad ,
												T3.estado ,
												T3.municipio ,
												T3.parroquia ,
												T3.calle_callejon_av_trs,
												T3.casa_edif,
												T3.escalera,
												T3.piso,
												T3.apartamento,
												T3.barrio_urb_zona,
												T3.direccion,
												T3.telefono_habitacion,
												T3.telefono_celular,
												T3.telefono_trabajo,
												T3.hora_contacto,
												T3.c4_nexo_familiar,
												T3.c5_grado_instruccion,
												T3.c6_situacion_ocupacion,
												T3.c7_tipo_vivienda,
												T3.c8_tenencia_vivienda,
												T3.c9_personas_viven_usted ,
												T3.c10_personas_menores_6 ,
												T3.c11_personas_menores_6_12 ,
												T3.c12_personas_menores_6_12_escuela,
												T3.c13_frecuencia_escuela,
												T3.c14_personas_ingresos ,
												T3.c15_ingreso_hogar,
												T3.c16_principal_hogar,
												T3.c17_familia_exterior,
												T3.c18_ayuda_economica_exterior,
												T3.c20_comidas_diarias,
												T3.c22_referido,
												T3.cl1_servicio,
												T3.cl2_canalizar,
												T3.cl3_solicitar,
												T3.cl4_asistencia,
												T3.cl5_tramite,
												T3.cl6_tribunales,
												T3.cl7_experiencia,
												T3.cl8_ddhh,
												T3.cl9_justicia,
												T3.cl10_transicional,
												T3.cs1_actividad,
												T3.cs3_capacidad,
												T3.cs5_contribuir,
												T3.cs7_participar_actividades,
												T3.cs8_ayuda_economica_exterior,
												T3.create_uid ,
												T3.create_date ,
												T3.write_uid ,
												T3.write_date 
																		FROM (
																		SELECT	T2.login,
																		T2.id ,
								T2.datos_jornada_calendario,
								T2.nombre,
								T2.apellido,
								T2.foto_carnet_clave,
								T2.nacionalidad_real,
								T2.cedula,
								T2.fecha_nacimiento,
								T2.email,
								T2.genero,
								T2.estado_civil,
								T2.nacionalidad ,
								T2.estado ,
								T2.municipio ,
								T2.parroquia ,
								T2.calle_callejon_av_trs,
								T2.casa_edif,
								T2.escalera,
								T2.piso,
								T2.apartamento,
								T2.barrio_urb_zona,
								T2.direccion,
								T2.telefono_habitacion,
								T2.telefono_celular,
								T2.telefono_trabajo,
								T2.hora_contacto,
								T2.c4_nexo_familiar,
								T2.c5_grado_instruccion,
								T2.c6_situacion_ocupacion,
								T2.c7_tipo_vivienda,
								T2.c8_tenencia_vivienda,
								T2.c9_personas_viven_usted ,
								T2.c10_personas_menores_6 ,
								T2.c11_personas_menores_6_12 ,
								T2.c12_personas_menores_6_12_escuela,
								T2.c13_frecuencia_escuela,
								T2.c14_personas_ingresos ,
								T2.c15_ingreso_hogar,
								T2.c16_principal_hogar,
								T2.c17_familia_exterior,
								T2.c18_ayuda_economica_exterior,
								T2.c20_comidas_diarias,
								T2.c22_referido,
								T2.cl1_servicio,
								T2.cl2_canalizar,
								T2.cl3_solicitar,
								T2.cl4_asistencia,
								T2.cl5_tramite,
								T2.cl6_tribunales,
								T2.cl7_experiencia,
								T2.cl8_ddhh,
								T2.cl9_justicia,
								T2.cl10_transicional,
								T2.cs1_actividad,
								T2.cs3_capacidad,
								T2.cs5_contribuir,
								T2.cs7_participar_actividades,
								T2.cs8_ayuda_economica_exterior,
								T2.create_uid ,
								T2.create_date ,
								T2.write_uid ,
								T2.write_date 
															FROM  dblink(   'host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 
																														'SELECT id ,
								datos_jornada_calendario,
								nombre,
								apellido,
								foto_carnet_clave,
								nacionalidad_real,
								cedula,
								fecha_nacimiento,
								email,
								genero,
								estado_civil,
								nacionalidad ,
								estado ,
								municipio ,
								parroquia ,
								calle_callejon_av_trs,
								casa_edif,
								escalera,
								piso,
								apartamento,
								barrio_urb_zona,
								direccion,
								telefono_habitacion,
								telefono_celular,
								telefono_trabajo,
								hora_contacto,
								c4_nexo_familiar,
								c5_grado_instruccion,
								c6_situacion_ocupacion,
								c7_tipo_vivienda,
								c8_tenencia_vivienda,
								c9_personas_viven_usted ,
								c10_personas_menores_6 ,
								c11_personas_menores_6_12 ,
								c12_personas_menores_6_12_escuela,
								c13_frecuencia_escuela,
								c14_personas_ingresos ,
								c15_ingreso_hogar,
								c16_principal_hogar,
								c17_familia_exterior,
								c18_ayuda_economica_exterior,
								c20_comidas_diarias,
								c22_referido,
								cl1_servicio,
								cl2_canalizar,
								cl3_solicitar,
								cl4_asistencia,
								cl5_tramite,
								cl6_tribunales,
								cl7_experiencia,
								cl8_ddhh,
								cl9_justicia,
								cl10_transicional,
								cs1_actividad,
								cs3_capacidad,
								cs5_contribuir,
								cs7_participar_actividades,
								cs8_ayuda_economica_exterior,
								create_uid ,
								create_date ,
								write_uid ,
								write_date 
																																FROM registro_asesoria')  AS t1(id integer,
								datos_jornada_calendario character varying,
								nombre character varying,
								apellido character varying,
								foto_carnet_clave text,
								nacionalidad_real character varying,
								cedula character varying,
								fecha_nacimiento date,
								email character varying,
								genero character varying,
								estado_civil character varying,
								nacionalidad integer,
								estado integer,
								municipio integer,
								parroquia integer,
								calle_callejon_av_trs character varying,
								casa_edif character varying,
								escalera character varying,
								piso character varying,
								apartamento character varying,
								barrio_urb_zona character varying,
								direccion text,
								telefono_habitacion character varying,
								telefono_celular character varying,
								telefono_trabajo character varying,
								hora_contacto character varying,
								c4_nexo_familiar character varying,
								c5_grado_instruccion character varying,
								c6_situacion_ocupacion character varying,
								c7_tipo_vivienda character varying,
								c8_tenencia_vivienda character varying,
								c9_personas_viven_usted integer,
								c10_personas_menores_6 integer,
								c11_personas_menores_6_12 integer,
								c12_personas_menores_6_12_escuela character varying,
								c13_frecuencia_escuela character varying,
								c14_personas_ingresos integer,
								c15_ingreso_hogar character varying,
								c16_principal_hogar character varying,
								c17_familia_exterior character varying,
								c18_ayuda_economica_exterior character varying,
								c20_comidas_diarias character varying,
								c22_referido character varying,
								cl1_servicio character varying,
								cl2_canalizar character varying,
								cl3_solicitar character varying,
								cl4_asistencia character varying,
								cl5_tramite character varying,
								cl6_tribunales character varying,
								cl7_experiencia character varying,
								cl8_ddhh character varying,
								cl9_justicia character varying,
								cl10_transicional character varying,
								cs1_actividad character varying,
								cs3_capacidad character varying,
								cs5_contribuir character varying,
								cs7_participar_actividades character varying,
								cs8_ayuda_economica_exterior text,
								create_uid integer,
								create_date timestamp,
								write_uid integer,
								write_date timestamp )
																								RIGHT JOIN 
									dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 
																														'SELECT   RU.login, 
																										CL.id  ,
								datos_jornada_calendario,
								nombre,
								apellido,
								foto_carnet_clave,
								nacionalidad_real,
								cedula,
								fecha_nacimiento,
								email,
								genero,
								estado_civil,
								nacionalidad ,
								estado ,
								municipio ,
								parroquia ,
								calle_callejon_av_trs,
								casa_edif,
								escalera,
								piso,
								apartamento,
								barrio_urb_zona,
								direccion,
								telefono_habitacion,
								telefono_celular,
								telefono_trabajo,
								hora_contacto,
								c4_nexo_familiar,
								c5_grado_instruccion,
								c6_situacion_ocupacion,
								c7_tipo_vivienda,
								c8_tenencia_vivienda,
								c9_personas_viven_usted ,
								c10_personas_menores_6 ,
								c11_personas_menores_6_12 ,
								c12_personas_menores_6_12_escuela,
								c13_frecuencia_escuela,
								c14_personas_ingresos ,
								c15_ingreso_hogar,
								c16_principal_hogar,
								c17_familia_exterior,
								c18_ayuda_economica_exterior,
								c20_comidas_diarias,
								c22_referido,
								cl1_servicio,
								cl2_canalizar,
								cl3_solicitar,
								cl4_asistencia,
								cl5_tramite,
								cl6_tribunales,
								cl7_experiencia,
								cl8_ddhh,
								cl9_justicia,
								cl10_transicional,
								cs1_actividad,
								cs3_capacidad,
								cs5_contribuir,
								cs7_participar_actividades,
								cs8_ayuda_economica_exterior,
                                                                                                    CL.create_uid , 
                                                                                                    CL.create_date, 
                                                                                                    CL.write_uid , 
                                                                                                    CL.write_date    
                                                                                            FROM registro_asesoria CL, res_users RU
                                                                                            WHERE CL.create_uid = RU.id')  AS t2(login character varying,
											id integer,
											datos_jornada_calendario character varying,
											nombre character varying,
											apellido character varying,
											foto_carnet_clave text,
											nacionalidad_real character varying,
											cedula character varying,
											fecha_nacimiento date,
											email character varying,
											genero character varying,
											estado_civil character varying,
											nacionalidad integer,
											estado integer,
											municipio integer,
											parroquia integer,
											calle_callejon_av_trs character varying,
											casa_edif character varying,
											escalera character varying,
											piso character varying,
											apartamento character varying,
											barrio_urb_zona character varying,
											direccion text,
											telefono_habitacion character varying,
											telefono_celular character varying,
											telefono_trabajo character varying,
											hora_contacto character varying,
											c4_nexo_familiar character varying,
											c5_grado_instruccion character varying,
											c6_situacion_ocupacion character varying,
											c7_tipo_vivienda character varying,
											c8_tenencia_vivienda character varying,
											c9_personas_viven_usted integer,
											c10_personas_menores_6 integer,
											c11_personas_menores_6_12 integer,
											c12_personas_menores_6_12_escuela character varying,
											c13_frecuencia_escuela character varying,
											c14_personas_ingresos integer,
											c15_ingreso_hogar character varying,
											c16_principal_hogar character varying,
											c17_familia_exterior character varying,
											c18_ayuda_economica_exterior character varying,
											c20_comidas_diarias character varying,
											c22_referido character varying,
											cl1_servicio character varying,
											cl2_canalizar character varying,
											cl3_solicitar character varying,
											cl4_asistencia character varying,
											cl5_tramite character varying,
											cl6_tribunales character varying,
											cl7_experiencia character varying,
											cl8_ddhh character varying,
											cl9_justicia character varying,
											cl10_transicional character varying,
											cs1_actividad character varying,
											cs3_capacidad character varying,
											cs5_contribuir character varying,
											cs7_participar_actividades character varying,
											cs8_ayuda_economica_exterior text,
											create_uid integer,
											create_date timestamp,
											write_uid integer,
											write_date timestamp )
																								ON T1.create_date = T2.create_date
                                                    WHERE T1.create_date IS NULL) T3, res_users RU
                            WHERE T3.LOGIN = RU.LOGIN

                                """ 
            cur.execute(sql)
            if cur.rowcount > 0:
                list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %(NOMBRE_TABLA))

                registro_asesorias = cur.fetchall()
                descripcion = cur.description
                values = []
                for registro_asesoria in registro_asesorias:
                    sql =   """ SELECT * 
                                FROM dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd',
                                            'SELECT cedula 
                                            FROM cedulas_venezuela_2012 
                                            WHERE cedula = %s ') as t1(A integer)
                            """ % (registro_asesoria[8])
                    cur.execute(sql)
                    # cr.execute(sql)
                    if cur.rowcount > 0:
                        cedula_existe_b = True
                    else:
                        cedula_existe_b = False
                        list_.append('Esta cédula [CI: %s Nom.: %s] se agregará en la tabla del cedulas_venezuela_2012 (%s)' %(registro_asesoria[8],registro_asesoria[4],cur.statusmessage))
                    
                    sql = """ 	SELECT *
                                FROM dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC',' 
                                select rac2.registro_cs2_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS2'' AS PREGUNTA, RA.NOMBRE
                                from registro_cs2 c2,registro_asesoria_registro_cs2_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cs2_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                UNION
                                select rac2.registro_cs4_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS4'' AS PREGUNTA, RA.NOMBRE
                                from registro_cs4 c2,registro_asesoria_registro_cs4_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cs4_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                UNION
                                select rac2.registro_cs6_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS6'' AS PREGUNTA, RA.NOMBRE
                                from registro_cs6 c2,registro_asesoria_registro_cs6_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cs6_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                UNION
                                select rac2.registro_cs9_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS9'' AS PREGUNTA, RA.NOMBRE
                                from registro_cs9 c2,registro_asesoria_registro_cs9_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cs9_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                UNION
                                select rac2.registro_cuestionario1_c19_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS19'' AS PREGUNTA, RA.NOMBRE
                                from registro_cuestionario1_c19 c2,registro_asesoria_registro_cuestionario1_c19_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cuestionario1_c19_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                UNION
                                select rac2.registro_cuestionario1_c21_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS21'' AS PREGUNTA, RA.NOMBRE
                                from registro_cuestionario1_c21 c2,registro_asesoria_registro_cuestionario1_c21_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cuestionario1_c21_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                ORDER BY PREGUNTA,REGISTRO_ASESORIA') AS T1 (A integer, B integer, C character varying, D character varying)
                                    """ % (	registro_asesoria[8],registro_asesoria[8],
                                            registro_asesoria[8],registro_asesoria[8],
                                            registro_asesoria[8],registro_asesoria[8])
                    # cur2.execute(sql)
                    cur.execute(sql)
                    if cur.rowcount > 0:
                        # if cur2.rowcount > 0:
                        registros = cur.fetchall()
                        # registros = cur2.fetchall()
                        CS2  = []
                        CS4  = []
                        CS6  = []
                        CS9  = []
                        CS19 = []
                        CS21 = []
                        for registro in registros:
                            if registro[2] == 'CS2':
                                CS2.append(registro[0])
                            if registro[2] == 'CS4':
                                CS4.append(registro[0])
                            if registro[2] == 'CS6':
                                CS6.append(registro[0])
                            if registro[2] == 'CS9':
                                CS9.append(registro[0])
                            if registro[2] == 'CS19':
                                CS19.append(registro[0])
                            if registro[2] == 'CS21':
                                CS21.append(registro[0])

                    values.append({
                        # 'id ':registro_asesoria[2],
                        'datos_jornada_calendario':registro_asesoria[3],
                        'nombre':registro_asesoria[4],
                        'apellido':registro_asesoria[5],
                        'foto_carnet_clave':registro_asesoria[6],
                        'nacionalidad_real':registro_asesoria[7],
                        'cedula':registro_asesoria[8],
                        'fecha_nacimiento':registro_asesoria[9],
                        'email':registro_asesoria[10],
                        'genero':registro_asesoria[11],
                        'estado_civil':registro_asesoria[12],
                        'nacionalidad':registro_asesoria[13],
                        'estado':registro_asesoria[14],
                        'municipio':registro_asesoria[15],
                        'parroquia':registro_asesoria[16],
                        'calle_callejon_av_trs':registro_asesoria[17],
                        'casa_edif':registro_asesoria[18],
                        'escalera':registro_asesoria[19],
                        'piso':registro_asesoria[20],
                        'apartamento':registro_asesoria[21],
                        'barrio_urb_zona':registro_asesoria[22],
                        'direccion':registro_asesoria[23],
                        'telefono_habitacion':registro_asesoria[24],
                        'telefono_celular':registro_asesoria[25],
                        'telefono_trabajo':registro_asesoria[26],
                        'hora_contacto':registro_asesoria[27],
                        'c4_nexo_familiar':registro_asesoria[28],
                        'c5_grado_instruccion':registro_asesoria[29],
                        'c6_situacion_ocupacion':registro_asesoria[30],
                        'c7_tipo_vivienda':registro_asesoria[31],
                        'c8_tenencia_vivienda':registro_asesoria[32],
                        'c9_personas_viven_usted':registro_asesoria[33],
                        'c10_personas_menores_6':registro_asesoria[34],
                        'c11_personas_menores_6_12':registro_asesoria[35],
                        'c12_personas_menores_6_12_escuela':registro_asesoria[36],
                        'c13_frecuencia_escuela':registro_asesoria[37],
                        'c14_personas_ingresos':registro_asesoria[38],
                        'c15_ingreso_hogar':registro_asesoria[39],
                        'c16_principal_hogar':registro_asesoria[40],
                        'c17_familia_exterior':registro_asesoria[41],
                        'c18_ayuda_economica_exterior':registro_asesoria[42],
                        'c20_comidas_diarias':registro_asesoria[43],
                        'c22_referido':registro_asesoria[44],
                        'cl1_servicio':registro_asesoria[45],
                        'cl2_canalizar':registro_asesoria[46],
                        'cl3_solicitar':registro_asesoria[47],
                        'cl4_asistencia':registro_asesoria[48],
                        'cl5_tramite':registro_asesoria[49],
                        'cl6_tribunales':registro_asesoria[50],
                        'cl7_experiencia':registro_asesoria[51],
                        'cl8_ddhh':registro_asesoria[52],
                        'cl9_justicia':registro_asesoria[53],
                        'cl10_transicional':registro_asesoria[54],
                        'cs1_actividad':registro_asesoria[55],
                        'cs3_capacidad':registro_asesoria[56],
                        'cs5_contribuir':registro_asesoria[57],
                        'cs7_participar_actividades':registro_asesoria[58],
                        'cs8_ayuda_economica_exterior':registro_asesoria[59],
                        'create_uid':registro_asesoria[60],
                        'create_date':registro_asesoria[61],
                        'write_uid':registro_asesoria[62],
                        'write_date':registro_asesoria[63],
                        'c19_beneficios_estado': [[6, False, CS19]],
                        'c21_principal_problema': [[6, False, CS21]],
                        'cs2_actividad_asistencia': [[6, False, CS2]],
                        'cs4_tribunales': [[6, False, CS4]],
                        'cs6_no_contribuir': [[6, False, CS6]],
                        'cs9_expectativas': [[6, False, CS9]],
                        'cedula_existe': cedula_existe_b,
				    })
                list_.append('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t %s' % (values, cur.statusmessage))
                _logger.info('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t %s' % (values, cur.statusmessage))

                record = self.env['registro.asesoria'].create(values)
                list_.append('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t' % (record))
                _logger.info('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t ' % (record))
                list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
                
                try:
                    list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %('registro_asesoria'))
                    
                    for registro_asesoria in registro_asesorias:
                        values_ = {
                            'create_uid':registro_asesoria[60],
                            'create_date':registro_asesoria[61],
                            # 'write_uid':registro_asesoria[62],
                            'write_date':registro_asesoria[63],
                        }
                        res = self.env['registro.asesoria'].search([('cedula','=',registro_asesoria[8])])
                        respuesta = res.write(values_)
                        # sql = ' UPDATE  %s SET ' % (NOMBRE_TABLA)
                        # sql = sql + 'create_uid=\'%s\', create_date=\'%s\', write_date=\'%s\'' % (registro_asesoria[0],
                        #                                                                             registro_asesoria[61],
                        #                                                                             registro_asesoria[63])
                        
                        # sql = sql + ' WHERE cedula=\'%s\' AND datos_jornada_calendario=\'%s\' '  % (registro_asesoria[8],
                        #                                                                             registro_asesoria[3])
                        
                        list_.append('respuesta = res.write(values_)........................................................................... 250 \t\t\t\t %s \t\t\t\t ' % (respuesta))
                        _logger.info('respuesta = res.write(values_)........................................................................... 250 \t\t\t\t %s \t\t\t\t ' % (respuesta))
                        cur.execute(sql)
                        # cr.execute(sql)
                        
                        if cur.rowcount > 0:
                        # if cr.rowcount > 0:
                            conexion.commit()
                            list_.append('Se actualizó el registro [CI: %s Nom.: %s] de la tabla << %s >> en la PC local (%s)' %(registro_asesoria[7],registro_asesoria[4],NOMBRE_TABLA,cur.statusmessage))
                        else:
                            list_.append('No hubo actualización en la tabla << %s >> de la PC local  para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                    list_.append('------------------------------------------------------------------------------------------------------------')
                    self.action_actualizar_registro_asesoria_write_uid()
                except (Exception, psycopg2.DatabaseError) as error:
                        list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                        _logger.info('....................................................................................................3 %s' % (error))
                
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
        
        # mostrar_resultados_update()

    #1.3 Prueba de registro asesoria nuevo 3 
    def action_bajar_registro_asesoria_3(self):
        
        NOMBRE_TABLA = 'public.registro_asesoria'
        # NOMBRE_TABLA_REAL = 'public.registro_asesoria_registro_cuestionario1_c21_rel'
        NOMBRE_FUNCION = 'action_bajar_registro_asesoria_3'
        list_.append('Inicio de la función # Prueba 3 << %s >>' % (NOMBRE_FUNCION))

        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        USER_LOCAL="openpg"
        PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
            cur = conexion.cursor()
            # cur2 = conexion.cursor()
            # cr = self.env.cr
            sql = """  		SELECT RU.id, 
																		T3.login,
																		T3.id ,
												T3.datos_jornada_calendario,
												T3.nombre,
												T3.apellido,
												T3.foto_carnet_clave,
												T3.nacionalidad_real,
												T3.cedula,
												T3.fecha_nacimiento,
												T3.email,
												T3.genero,
												T3.estado_civil,
												T3.nacionalidad ,
												T3.estado ,
												T3.municipio ,
												T3.parroquia ,
												T3.calle_callejon_av_trs,
												T3.casa_edif,
												T3.escalera,
												T3.piso,
												T3.apartamento,
												T3.barrio_urb_zona,
												T3.direccion,
												T3.telefono_habitacion,
												T3.telefono_celular,
												T3.telefono_trabajo,
												T3.hora_contacto,
												T3.c4_nexo_familiar,
												T3.c5_grado_instruccion,
												T3.c6_situacion_ocupacion,
												T3.c7_tipo_vivienda,
												T3.c8_tenencia_vivienda,
												T3.c9_personas_viven_usted ,
												T3.c10_personas_menores_6 ,
												T3.c11_personas_menores_6_12 ,
												T3.c12_personas_menores_6_12_escuela,
												T3.c13_frecuencia_escuela,
												T3.c14_personas_ingresos ,
												T3.c15_ingreso_hogar,
												T3.c16_principal_hogar,
												T3.c17_familia_exterior,
												T3.c18_ayuda_economica_exterior,
												T3.c20_comidas_diarias,
												T3.c22_referido,
												T3.cl1_servicio,
												T3.cl2_canalizar,
												T3.cl3_solicitar,
												T3.cl4_asistencia,
												T3.cl5_tramite,
												T3.cl6_tribunales,
												T3.cl7_experiencia,
												T3.cl8_ddhh,
												T3.cl9_justicia,
												T3.cl10_transicional,
												T3.cs1_actividad,
												T3.cs3_capacidad,
												T3.cs5_contribuir,
												T3.cs7_participar_actividades,
												T3.cs8_ayuda_economica_exterior,
												T3.create_uid ,
												T3.create_date ,
												T3.write_uid ,
												T3.write_date 
																		FROM (
																		SELECT	T2.login,
																		T2.id ,
								T2.datos_jornada_calendario,
								T2.nombre,
								T2.apellido,
								T2.foto_carnet_clave,
								T2.nacionalidad_real,
								T2.cedula,
								T2.fecha_nacimiento,
								T2.email,
								T2.genero,
								T2.estado_civil,
								T2.nacionalidad ,
								T2.estado ,
								T2.municipio ,
								T2.parroquia ,
								T2.calle_callejon_av_trs,
								T2.casa_edif,
								T2.escalera,
								T2.piso,
								T2.apartamento,
								T2.barrio_urb_zona,
								T2.direccion,
								T2.telefono_habitacion,
								T2.telefono_celular,
								T2.telefono_trabajo,
								T2.hora_contacto,
								T2.c4_nexo_familiar,
								T2.c5_grado_instruccion,
								T2.c6_situacion_ocupacion,
								T2.c7_tipo_vivienda,
								T2.c8_tenencia_vivienda,
								T2.c9_personas_viven_usted ,
								T2.c10_personas_menores_6 ,
								T2.c11_personas_menores_6_12 ,
								T2.c12_personas_menores_6_12_escuela,
								T2.c13_frecuencia_escuela,
								T2.c14_personas_ingresos ,
								T2.c15_ingreso_hogar,
								T2.c16_principal_hogar,
								T2.c17_familia_exterior,
								T2.c18_ayuda_economica_exterior,
								T2.c20_comidas_diarias,
								T2.c22_referido,
								T2.cl1_servicio,
								T2.cl2_canalizar,
								T2.cl3_solicitar,
								T2.cl4_asistencia,
								T2.cl5_tramite,
								T2.cl6_tribunales,
								T2.cl7_experiencia,
								T2.cl8_ddhh,
								T2.cl9_justicia,
								T2.cl10_transicional,
								T2.cs1_actividad,
								T2.cs3_capacidad,
								T2.cs5_contribuir,
								T2.cs7_participar_actividades,
								T2.cs8_ayuda_economica_exterior,
								T2.create_uid ,
								T2.create_date ,
								T2.write_uid ,
								T2.write_date 
															FROM  dblink(   'host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 
																														'SELECT id ,
								datos_jornada_calendario,
								nombre,
								apellido,
								foto_carnet_clave,
								nacionalidad_real,
								cedula,
								fecha_nacimiento,
								email,
								genero,
								estado_civil,
								nacionalidad ,
								estado ,
								municipio ,
								parroquia ,
								calle_callejon_av_trs,
								casa_edif,
								escalera,
								piso,
								apartamento,
								barrio_urb_zona,
								direccion,
								telefono_habitacion,
								telefono_celular,
								telefono_trabajo,
								hora_contacto,
								c4_nexo_familiar,
								c5_grado_instruccion,
								c6_situacion_ocupacion,
								c7_tipo_vivienda,
								c8_tenencia_vivienda,
								c9_personas_viven_usted ,
								c10_personas_menores_6 ,
								c11_personas_menores_6_12 ,
								c12_personas_menores_6_12_escuela,
								c13_frecuencia_escuela,
								c14_personas_ingresos ,
								c15_ingreso_hogar,
								c16_principal_hogar,
								c17_familia_exterior,
								c18_ayuda_economica_exterior,
								c20_comidas_diarias,
								c22_referido,
								cl1_servicio,
								cl2_canalizar,
								cl3_solicitar,
								cl4_asistencia,
								cl5_tramite,
								cl6_tribunales,
								cl7_experiencia,
								cl8_ddhh,
								cl9_justicia,
								cl10_transicional,
								cs1_actividad,
								cs3_capacidad,
								cs5_contribuir,
								cs7_participar_actividades,
								cs8_ayuda_economica_exterior,
								create_uid ,
								create_date ,
								write_uid ,
								write_date 
																																FROM registro_asesoria')  AS t1(id integer,
								datos_jornada_calendario character varying,
								nombre character varying,
								apellido character varying,
								foto_carnet_clave text,
								nacionalidad_real character varying,
								cedula character varying,
								fecha_nacimiento date,
								email character varying,
								genero character varying,
								estado_civil character varying,
								nacionalidad integer,
								estado integer,
								municipio integer,
								parroquia integer,
								calle_callejon_av_trs character varying,
								casa_edif character varying,
								escalera character varying,
								piso character varying,
								apartamento character varying,
								barrio_urb_zona character varying,
								direccion text,
								telefono_habitacion character varying,
								telefono_celular character varying,
								telefono_trabajo character varying,
								hora_contacto character varying,
								c4_nexo_familiar character varying,
								c5_grado_instruccion character varying,
								c6_situacion_ocupacion character varying,
								c7_tipo_vivienda character varying,
								c8_tenencia_vivienda character varying,
								c9_personas_viven_usted integer,
								c10_personas_menores_6 integer,
								c11_personas_menores_6_12 integer,
								c12_personas_menores_6_12_escuela character varying,
								c13_frecuencia_escuela character varying,
								c14_personas_ingresos integer,
								c15_ingreso_hogar character varying,
								c16_principal_hogar character varying,
								c17_familia_exterior character varying,
								c18_ayuda_economica_exterior character varying,
								c20_comidas_diarias character varying,
								c22_referido character varying,
								cl1_servicio character varying,
								cl2_canalizar character varying,
								cl3_solicitar character varying,
								cl4_asistencia character varying,
								cl5_tramite character varying,
								cl6_tribunales character varying,
								cl7_experiencia character varying,
								cl8_ddhh character varying,
								cl9_justicia character varying,
								cl10_transicional character varying,
								cs1_actividad character varying,
								cs3_capacidad character varying,
								cs5_contribuir character varying,
								cs7_participar_actividades character varying,
								cs8_ayuda_economica_exterior text,
								create_uid integer,
								create_date timestamp,
								write_uid integer,
								write_date timestamp )
																								RIGHT JOIN 
									dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC', 
																														'SELECT   RU.login, 
																										CL.id  ,
								datos_jornada_calendario,
								nombre,
								apellido,
								foto_carnet_clave,
								nacionalidad_real,
								cedula,
								fecha_nacimiento,
								email,
								genero,
								estado_civil,
								nacionalidad ,
								estado ,
								municipio ,
								parroquia ,
								calle_callejon_av_trs,
								casa_edif,
								escalera,
								piso,
								apartamento,
								barrio_urb_zona,
								direccion,
								telefono_habitacion,
								telefono_celular,
								telefono_trabajo,
								hora_contacto,
								c4_nexo_familiar,
								c5_grado_instruccion,
								c6_situacion_ocupacion,
								c7_tipo_vivienda,
								c8_tenencia_vivienda,
								c9_personas_viven_usted ,
								c10_personas_menores_6 ,
								c11_personas_menores_6_12 ,
								c12_personas_menores_6_12_escuela,
								c13_frecuencia_escuela,
								c14_personas_ingresos ,
								c15_ingreso_hogar,
								c16_principal_hogar,
								c17_familia_exterior,
								c18_ayuda_economica_exterior,
								c20_comidas_diarias,
								c22_referido,
								cl1_servicio,
								cl2_canalizar,
								cl3_solicitar,
								cl4_asistencia,
								cl5_tramite,
								cl6_tribunales,
								cl7_experiencia,
								cl8_ddhh,
								cl9_justicia,
								cl10_transicional,
								cs1_actividad,
								cs3_capacidad,
								cs5_contribuir,
								cs7_participar_actividades,
								cs8_ayuda_economica_exterior,
                                                                                                    CL.create_uid , 
                                                                                                    CL.create_date, 
                                                                                                    CL.write_uid , 
                                                                                                    CL.write_date    
                                                                                            FROM registro_asesoria CL, res_users RU
                                                                                            WHERE CL.create_uid = RU.id')  AS t2(login character varying,
											id integer,
											datos_jornada_calendario character varying,
											nombre character varying,
											apellido character varying,
											foto_carnet_clave text,
											nacionalidad_real character varying,
											cedula character varying,
											fecha_nacimiento date,
											email character varying,
											genero character varying,
											estado_civil character varying,
											nacionalidad integer,
											estado integer,
											municipio integer,
											parroquia integer,
											calle_callejon_av_trs character varying,
											casa_edif character varying,
											escalera character varying,
											piso character varying,
											apartamento character varying,
											barrio_urb_zona character varying,
											direccion text,
											telefono_habitacion character varying,
											telefono_celular character varying,
											telefono_trabajo character varying,
											hora_contacto character varying,
											c4_nexo_familiar character varying,
											c5_grado_instruccion character varying,
											c6_situacion_ocupacion character varying,
											c7_tipo_vivienda character varying,
											c8_tenencia_vivienda character varying,
											c9_personas_viven_usted integer,
											c10_personas_menores_6 integer,
											c11_personas_menores_6_12 integer,
											c12_personas_menores_6_12_escuela character varying,
											c13_frecuencia_escuela character varying,
											c14_personas_ingresos integer,
											c15_ingreso_hogar character varying,
											c16_principal_hogar character varying,
											c17_familia_exterior character varying,
											c18_ayuda_economica_exterior character varying,
											c20_comidas_diarias character varying,
											c22_referido character varying,
											cl1_servicio character varying,
											cl2_canalizar character varying,
											cl3_solicitar character varying,
											cl4_asistencia character varying,
											cl5_tramite character varying,
											cl6_tribunales character varying,
											cl7_experiencia character varying,
											cl8_ddhh character varying,
											cl9_justicia character varying,
											cl10_transicional character varying,
											cs1_actividad character varying,
											cs3_capacidad character varying,
											cs5_contribuir character varying,
											cs7_participar_actividades character varying,
											cs8_ayuda_economica_exterior text,
											create_uid integer,
											create_date timestamp,
											write_uid integer,
											write_date timestamp )
																								ON T1.create_date = T2.create_date
                                                    WHERE T1.create_date IS NULL) T3, res_users RU
                            WHERE T3.LOGIN = RU.LOGIN

                                """ 
            cur.execute(sql)
            if cur.rowcount > 0:
                list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %(NOMBRE_TABLA))

                registro_asesorias = cur.fetchall()
                descripcion = cur.description
                values = []
                for registro_asesoria in registro_asesorias:
                    # sql =   """ SELECT * 
                    #             FROM dblink('host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd',
                    #                         'SELECT cedula 
                    #                         FROM cedulas_venezuela_2012 
                    #                         WHERE cedula = %s ') as t1(A integer)
                    #         """ % (registro_asesoria[8])
                    # cur.execute(sql)
                    # if cur.rowcount > 0:
                    #     cedula_existe_b = True
                    # else:
                    #     cedula_existe_b = False
                    #     list_.append('Esta cédula [CI: %s Nom.: %s] se agregará en la tabla del cedulas_venezuela_2012 (%s)' %(registro_asesoria[8],registro_asesoria[4],cur.statusmessage))
                    
                    sql = """ 	SELECT *
                                FROM dblink('host=34.68.236.125 dbname=bitnami_odoo user=postgres password=gmWC3QAUudPC',' 
                                select rac2.registro_cs2_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS2'' AS PREGUNTA, RA.NOMBRE
                                from registro_cs2 c2,registro_asesoria_registro_cs2_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cs2_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                UNION
                                select rac2.registro_cs4_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS4'' AS PREGUNTA, RA.NOMBRE
                                from registro_cs4 c2,registro_asesoria_registro_cs4_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cs4_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                UNION
                                select rac2.registro_cs6_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS6'' AS PREGUNTA, RA.NOMBRE
                                from registro_cs6 c2,registro_asesoria_registro_cs6_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cs6_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                UNION
                                select rac2.registro_cs9_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS9'' AS PREGUNTA, RA.NOMBRE
                                from registro_cs9 c2,registro_asesoria_registro_cs9_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cs9_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                UNION
                                select rac2.registro_cuestionario1_c19_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS19'' AS PREGUNTA, RA.NOMBRE
                                from registro_cuestionario1_c19 c2,registro_asesoria_registro_cuestionario1_c19_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cuestionario1_c19_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                UNION
                                select rac2.registro_cuestionario1_c21_id AS REGISTRO, rac2.registro_asesoria_id AS REGISTRO_ASESORIA, ''CS21'' AS PREGUNTA, RA.NOMBRE
                                from registro_cuestionario1_c21 c2,registro_asesoria_registro_cuestionario1_c21_rel rac2, registro_asesoria ra
                                where c2.id =  rac2.registro_cuestionario1_c21_id
                                    AND RA.ID = rac2.registro_asesoria_id
                                    AND RA.CEDULA = \'\'%s\'\'
                                ORDER BY PREGUNTA,REGISTRO_ASESORIA') AS T1 (A integer, B integer, C character varying, D character varying)
                                    """ % (	registro_asesoria[8],registro_asesoria[8],
                                            registro_asesoria[8],registro_asesoria[8],
                                            registro_asesoria[8],registro_asesoria[8])
                    # cur2.execute(sql)
                    cur.execute(sql)
                    if cur.rowcount > 0:
                        # if cur2.rowcount > 0:
                        registros = cur.fetchall()
                        # registros = cur2.fetchall()
                        CS2  = []
                        CS4  = []
                        CS6  = []
                        CS9  = []
                        CS19 = []
                        CS21 = []
                        for registro in registros:
                            if registro[2] == 'CS2':
                                CS2.append(registro[0])
                            if registro[2] == 'CS4':
                                CS4.append(registro[0])
                            if registro[2] == 'CS6':
                                CS6.append(registro[0])
                            if registro[2] == 'CS9':
                                CS9.append(registro[0])
                            if registro[2] == 'CS19':
                                CS19.append(registro[0])
                            if registro[2] == 'CS21':
                                CS21.append(registro[0])

                    values.append({
                        # 'id ':registro_asesoria[2],
                        'datos_jornada_calendario':registro_asesoria[3],
                        'nombre':registro_asesoria[4],
                        'apellido':registro_asesoria[5],
                        'foto_carnet_clave':registro_asesoria[6],
                        'nacionalidad_real':registro_asesoria[7],
                        'cedula':registro_asesoria[8],
                        'fecha_nacimiento':registro_asesoria[9],
                        'email':registro_asesoria[10],
                        'genero':registro_asesoria[11],
                        'estado_civil':registro_asesoria[12],
                        'nacionalidad':registro_asesoria[13],
                        'estado':registro_asesoria[14],
                        'municipio':registro_asesoria[15],
                        'parroquia':registro_asesoria[16],
                        'calle_callejon_av_trs':registro_asesoria[17],
                        'casa_edif':registro_asesoria[18],
                        'escalera':registro_asesoria[19],
                        'piso':registro_asesoria[20],
                        'apartamento':registro_asesoria[21],
                        'barrio_urb_zona':registro_asesoria[22],
                        'direccion':registro_asesoria[23],
                        'telefono_habitacion':registro_asesoria[24],
                        'telefono_celular':registro_asesoria[25],
                        'telefono_trabajo':registro_asesoria[26],
                        'hora_contacto':registro_asesoria[27],
                        'c4_nexo_familiar':registro_asesoria[28],
                        'c5_grado_instruccion':registro_asesoria[29],
                        'c6_situacion_ocupacion':registro_asesoria[30],
                        'c7_tipo_vivienda':registro_asesoria[31],
                        'c8_tenencia_vivienda':registro_asesoria[32],
                        'c9_personas_viven_usted':registro_asesoria[33],
                        'c10_personas_menores_6':registro_asesoria[34],
                        'c11_personas_menores_6_12':registro_asesoria[35],
                        'c12_personas_menores_6_12_escuela':registro_asesoria[36],
                        'c13_frecuencia_escuela':registro_asesoria[37],
                        'c14_personas_ingresos':registro_asesoria[38],
                        'c15_ingreso_hogar':registro_asesoria[39],
                        'c16_principal_hogar':registro_asesoria[40],
                        'c17_familia_exterior':registro_asesoria[41],
                        'c18_ayuda_economica_exterior':registro_asesoria[42],
                        'c20_comidas_diarias':registro_asesoria[43],
                        'c22_referido':registro_asesoria[44],
                        'cl1_servicio':registro_asesoria[45],
                        'cl2_canalizar':registro_asesoria[46],
                        'cl3_solicitar':registro_asesoria[47],
                        'cl4_asistencia':registro_asesoria[48],
                        'cl5_tramite':registro_asesoria[49],
                        'cl6_tribunales':registro_asesoria[50],
                        'cl7_experiencia':registro_asesoria[51],
                        'cl8_ddhh':registro_asesoria[52],
                        'cl9_justicia':registro_asesoria[53],
                        'cl10_transicional':registro_asesoria[54],
                        'cs1_actividad':registro_asesoria[55],
                        'cs3_capacidad':registro_asesoria[56],
                        'cs5_contribuir':registro_asesoria[57],
                        'cs7_participar_actividades':registro_asesoria[58],
                        'cs8_ayuda_economica_exterior':registro_asesoria[59],
                        'create_uid':registro_asesoria[60],
                        'create_date':registro_asesoria[61],
                        'write_uid':registro_asesoria[62],
                        'write_date':registro_asesoria[63],
                        'c19_beneficios_estado': [[6, False, CS19]],
                        'c21_principal_problema': [[6, False, CS21]],
                        'cs2_actividad_asistencia': [[6, False, CS2]],
                        'cs4_tribunales': [[6, False, CS4]],
                        'cs6_no_contribuir': [[6, False, CS6]],
                        'cs9_expectativas': [[6, False, CS9]],
                        'cedula_existe': cedula_existe_b,
				    })
                list_.append('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t %s' % (values, cur.statusmessage))
                _logger.info('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t %s' % (values, cur.statusmessage))

                record = self.env['registro.asesoria'].create(values)
                list_.append('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t' % (record))
                _logger.info('Que carajo hace esto con los values........................................................................... 100 \t\t\t\t %s \t\t\t\t ' % (record))
                list_.append('Se insertó en la tabla << %s >> de la PC local (%s) registros' %(NOMBRE_TABLA,cur.statusmessage))
                
                try:
                    list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %('registro_asesoria'))
                    
                    for registro_asesoria in registro_asesorias:
                        values_ = {
                            'create_uid':registro_asesoria[60],
                            'create_date':registro_asesoria[61],
                            # 'write_uid':registro_asesoria[62],
                            'write_date':registro_asesoria[63],
                        }
                        res = self.env['registro.asesoria'].search([('cedula','=',registro_asesoria[8])])
                        respuesta = res.write(values_)
                        # sql = ' UPDATE  %s SET ' % (NOMBRE_TABLA)
                        # sql = sql + 'create_uid=\'%s\', create_date=\'%s\', write_date=\'%s\'' % (registro_asesoria[0],
                        #                                                                             registro_asesoria[61],
                        #                                                                             registro_asesoria[63])
                        
                        # sql = sql + ' WHERE cedula=\'%s\' AND datos_jornada_calendario=\'%s\' '  % (registro_asesoria[8],
                        #                                                                             registro_asesoria[3])
                        
                        list_.append('respuesta = res.write(values_)........................................................................... 250 \t\t\t\t %s \t\t\t\t ' % (respuesta))
                        _logger.info('respuesta = res.write(values_)........................................................................... 250 \t\t\t\t %s \t\t\t\t ' % (respuesta))
                        cur.execute(sql)
                        # cr.execute(sql)
                        
                        if cur.rowcount > 0:
                        # if cr.rowcount > 0:
                            conexion.commit()
                            list_.append('Se actualizó el registro [CI: %s Nom.: %s] de la tabla << %s >> en la PC local (%s)' %(registro_asesoria[7],registro_asesoria[4],NOMBRE_TABLA,cur.statusmessage))
                        else:
                            list_.append('No hubo actualización en la tabla << %s >> de la PC local  para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                    list_.append('------------------------------------------------------------------------------------------------------------')
                    self.action_actualizar_registro_asesoria_write_uid()
                except (Exception, psycopg2.DatabaseError) as error:
                        list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función action_actualizar_casos_legal' % (error, NOMBRE_TABLA))
                        _logger.info('....................................................................................................3 %s' % (error))
                
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
        
        # mostrar_resultados_update()

    #-----------------------------------------------------------------------------------------------
    def actualizar_transaccion_sincronizada(self):
            
        NOMBRE_TABLA = 'public.provene_transaccion_bd'
        NOMBRE_FUNCION = 'actualizar_transaccion_sincronizada'
        list_.append('Inicio de la función # 2.0 << %s >>' % (NOMBRE_FUNCION))

        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        USER_LOCAL="openpg"
        PASSWORD_LOCAL="openpgpwd"
    
        HOST_SERVER="127.0.0.1"
        DATABASE_SERVER="provene_local_6_1"
        USER_SERVER="openpg"
        PASSWORD_SERVER="openpgpwd"

        try:
            conexion_l = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
            conexion_s = psycopg2.connect(host=HOST_SERVER, database=DATABASE_SERVER, user=USER_SERVER, password=PASSWORD_SERVER)       
            curl = conexion_l.cursor()
            curs = conexion_s.cursor()
    
            sql = 	"""	SELECT 	T2.id,
                                T2.name,
                                T2.modelo_transaccion, 
                                T2.metodo_transaccion, 
                                T2.values_transaccion, 
                                T2.transaccion_sincronizada
                        FROM  	dblink( 'host=127.0.0.1 dbname=provene_local_6 user=openpg password=openpgpwd', 
                                        'SELECT id ,
                                                name, 
                                                modelo_transaccion ,
                                                metodo_transaccion ,
                                                values_transaccion ,
                                                transaccion_sincronizada
                                                FROM provene_transaccion_bd
                                                WHERE transaccion_sincronizada = False') AS t1(	id integer,
                                                                                                name character varying ,
                                                                                                modelo_transaccion character varying ,
                                                                                                metodo_transaccion character varying ,
                                                                                                values_transaccion character varying ,
                                                                                                transaccion_sincronizada boolean )
                        INNER JOIN 
                                dblink( 'host=127.0.0.1 dbname=provene_local_6_1 user=openpg password=openpgpwd',  
                                        'SELECT id ,
                                                name, 
                                                modelo_transaccion ,
                                                metodo_transaccion ,
                                                values_transaccion ,
                                                transaccion_sincronizada
                                                FROM provene_transaccion_bd
                                                WHERE transaccion_sincronizada = False') AS t2(	id integer,
                                                                                                name character varying ,
                                                                                                modelo_transaccion character varying ,
                                                                                                metodo_transaccion character varying ,
                                                                                                values_transaccion character varying ,
                                                                                                transaccion_sincronizada boolean )
                        ON T1.values_transaccion = T2.values_transaccion

                    """ 
            curl.execute(sql)
            if curl.rowcount > 0:
                list_.append('La consulta encontró coincidencias entre las tablas << %s >> del servidor y la local' %(NOMBRE_TABLA))

                registros = curl.fetchall()
                try:
                    for registro in registros:
                        r = registro[4]
                        r = r.replace('\'','\'\'')
                        sql = ' UPDATE  %s SET transaccion_sincronizada=True ' % (NOMBRE_TABLA)
                        sql = sql + ' WHERE values_transaccion=\'%s\' AND transaccion_sincronizada=False '  % (r)
                        
                        # list_.append('respuesta = res.write(values_)........................................................................... 250 \t\t\t\t %s \t\t\t\t ' % (sql))
                        _logger.info('SQL........................................................................... 250 \t\t\t\t %s \t\t\t\t ' % (sql))
                        curl.execute(sql)
                        
                        if curl.rowcount > 0:
                            conexion_l.commit()
                            list_.append('Se actualizó el registro [values: %s] de la tabla << %s >> en la PC local (%s)' %(registro[4],NOMBRE_TABLA,curl.statusmessage))
                        else:
                            list_.append('No hubo actualización en la tabla << %s >> de la PC local  para este caso (%s)' %(NOMBRE_TABLA,curl.statusmessage))
                    list_.append('------------------------------------------------------------------------------------------------------------')
                except (Exception, psycopg2.DatabaseError) as error:
                        list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA, NOMBRE_FUNCION))
                        _logger.info('....................................................................................................3 %s' % (error))
                try:
                    for registro in registros:
                        r = registro[4]
                        r = r.replace('\'','\'\'')
                        sql = ' UPDATE  %s SET transaccion_sincronizada=True ' % (NOMBRE_TABLA)
                        sql = sql + ' WHERE values_transaccion=\'%s\' AND transaccion_sincronizada=False '  % (r)
                        
                        # list_.append('respuesta = res.write(values_)........................................................................... 250 \t\t\t\t %s \t\t\t\t ' % (sql))
                        _logger.info('SQL........................................................................... 250 \t\t\t\t %s \t\t\t\t ' % (sql))
                        curs.execute(sql)
                        
                        if curs.rowcount > 0:
                            conexion_s.commit()
                            list_.append('Se actualizó el registro [values: %s] de la tabla << %s >> en el Servidor (%s)' %(registro[4],NOMBRE_TABLA,curs.statusmessage))
                        else:
                            list_.append('No hubo actualización en la tabla << %s >> en el Servidor para este caso (%s)' %(NOMBRE_TABLA,curs.statusmessage))
                    list_.append('------------------------------------------------------------------------------------------------------------')
                except (Exception, psycopg2.DatabaseError) as error:
                        list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA,NOMBRE_FUNCION))
                        _logger.info('....................................................................................................3 %s' % (error))
            
            else:
                list_.append('No hubo inserciones en las tablas << %s >> del servidor y la local (%s)' %(NOMBRE_TABLA,curl.statusmessage))
                _logger.info('Casos Legales........................................................................... 1 %s' % (curl.statusmessage))
        except (Exception, psycopg2.DatabaseError) as error:
            list_.append('Error: (%s). Al intentar actualizar la tabla << %s >> con la función %s' %(error, NOMBRE_TABLA, NOMBRE_FUNCION))
            _logger.info('Que carajo hace esto con los values........................................................................... 3 %s' % (error))
        except Exception as exc:
            list_.append('Error: %s' % (exc))
        finally:
            curl.close()
            curs.close()
            conexion_l.close()
            conexion_s.close()
            
    def reenmplazar_password(self):
        NOMBRE_TABLA = 'public.res_users'
        NOMBRE_FUNCION = 'reenmplazar_password'
        list_.append('Inicio de la función # 1.2 << %s >>' % (NOMBRE_FUNCION))
        
        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        USER_LOCAL="openpg"
        PASSWORD_LOCAL="openpgpwd"

        try:
            conexion = psycopg2.connect(host=HOST_LOCAL, database=DATABASE_LOCAL, user=USER_LOCAL, password=PASSWORD_LOCAL)       
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
                                            aceptar_manifiesto varchar)
                                """
            cur.execute(sql)
            if cur.rowcount > 0:
                list_.append('La consulta encontró en la tabla << %s >>, datos en el servidor que aún no estan en la PC local' %(NOMBRE_TABLA))
                
                campo_actualizar = cur.fetchall()
                descripcion = cur.description
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
                        list_.append('Se actualizó el registro [login: %s] de la tabla << %s >> en la PC local (%s)' %(update_casos_legal[2],NOMBRE_TABLA,cur.statusmessage))
                        _logger.info('........................................................................... 1 %s TABLA %s en la funcion: %s' % (cur.statusmessage,NOMBRE_TABLA, NOMBRE_FUNCION))
                    else:
                        _logger.info('........................................................................... 2 %s TABLA %s en la funcion: %s' % (cur.statusmessage,NOMBRE_TABLA, NOMBRE_FUNCION))
                        list_.append('No hubo actualización en la tabla << %s >> de la PC local  para este caso (%s)' %(NOMBRE_TABLA,cur.statusmessage))
                list_.append('------------------------------------------------------------------------------------------------------------')
            else:
                _logger.info('........................................................................... 2 %s' % (cur.statusmessage))
                list_.append('La consulta NO encontró diferencias entre la tabla << %s >> del Servidor y la PC local (%s)' %(NOMBRE_TABLA,cur.statusmessage))			
                
        except (Exception, psycopg2.DatabaseError) as error:
            list_.append('Error: %s. Al intentar actualizar los registros de la tabla << %s >> con la función %s' % (error, NOMBRE_TABLA,NOMBRE_FUNCION))
            _logger.info('........................................................................... 3 %s TABLA %s en la funcion: %s' % (error,NOMBRE_TABLA, NOMBRE_FUNCION))
        except Exception as exc:
            list_.append('Error: %s' % (exc))

    def sincronizar_transacciones(self):
        HOST_SERVER="127.0.0.1"
        DATABASE_SERVER="provene_local_6_1"
        # DATABASE_SERVER="provene_local_6"
        USER_SERVER="user@example.com"
        PASSWORD_SERVER="1234"
        PORT_SERVER = 8069

        HOST_LOCAL="127.0.0.1"
        DATABASE_LOCAL="provene_local_6"
        # DATABASE_LOCAL="provene_local_6_1"
        USER_LOCAL="user@example.com"
        PASSWORD_LOCAL="1234"
        PORT_LOCAL = 8069

        # HOST_SERVER="34.68.236.125"
        # DATABASE_SERVER="bitnami_odoo"
        # USER_SERVER="user@example.com"
        # PASSWORD_SERVER="gmWC3QAUudPC"
        # PORT_SERVER = 80

        # HOST_LOCAL="34.68.236.125"
        # DATABASE_LOCAL="bitnami_odoo"
        # USER_LOCAL="user@example.com"
        # PASSWORD_LOCAL="gmWC3QAUudPC"
        # PORT = 80


        odoo_s = odoorpc.ODOO(HOST_SERVER, port=PORT_SERVER)
        # odoo_l = odoorpc.ODOO(HOST_LOCAL, port=PORT_LOCAL)
        odoo_user = odoorpc.ODOO(HOST_LOCAL, port=PORT_LOCAL)

        # Login
        odoo_s.login(DATABASE_SERVER, USER_SERVER,PASSWORD_SERVER )
        # odoo_l.login(DATABASE_LOCAL, USER_LOCAL,PASSWORD_LOCAL )

        user_data = odoo_s.env['provene.transaccion.bd']
        registros = user_data.search([('transaccion_sincronizada','=',False)])
        campos = user_data.browse(registros)

        for value in campos:
            try:
                ejecutar = True
                values = ast.literal_eval(value.values_transaccion)
                modelo = str(value.modelo_transaccion)
                metodo = str(value.metodo_transaccion)
        
                registros_s = odoo_s.execute('res.users', 'read', int(value.create_uid.id))[0]
                login_s = registros_s['login']

                odoo_user.login(DATABASE_LOCAL, login_s,PASSWORD_LOCAL )
            
                if metodo == 'create':
                    modelo_s = odoo_s.env[modelo]
                    if modelo == 'registro.asesoria':
                        jornada_s = odoo_s.execute(modelo, 'read', ast.literal_eval(value.registro_id))
                        values['datos_jornada_calendario'] = jornada_s[0]['datos_jornada_calendario']
                        values_transaccion_s = {'values_transaccion':values}
                        cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, values_transaccion_s)
                    if modelo == 'registro.pasajeros.actividad.social':
                        actividad_area_social_s = odoo_s.execute('registro.actividad.social', 'read', values['actividad_id'])
                        registro_asesoria_calendario_s = odoo_s.execute('registro.asesoria.calendario', 'read', actividad_area_social_s[0]['actividad_area_social'][0])[0]
                        
                        modelo_l = odoo_user.env['registro.asesoria.calendario'].search([('name','=',registro_asesoria_calendario_s['name']),('tipo_actividad','=',registro_asesoria_calendario_s['tipo_actividad'])])
                        if len(modelo_l) > 0:
                            for id_l in modelo_l:
                                id_l_l = odoo_user.env['registro.actividad.social'].search([('actividad_area_social','=',id_l)])[0]
                                values['actividad_id'] = id_l_l
                                values_transaccion_s = {'values_transaccion':values}
                                cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, values_transaccion_s)
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
                            values_transaccion_s = {'values_transaccion':values}
                            cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, values_transaccion_s)
                        else:
                            ejecutar = False
            
                    if ejecutar:
                        resulado = odoo_user.execute(modelo, metodo, values)
                        list_.append('Se creó el registro %s la tabla << %s >> con el metodo %s' % (resulado,modelo,metodo))

                
                if metodo == 'write':
                    modelo_s = odoo_s.env[modelo]
                    cedula_s = odoo_s.execute(modelo, 'read', ast.literal_eval(value.registro_id))
            
                    modelo_l = odoo_user.env[modelo]
                    if modelo == 'registro.asesoria':
                        modelo_l = modelo_l.search([('cedula','=',cedula_s[0]['cedula'])])
                        registro_modelo = cedula_s[0]['cedula']
            
                    if modelo == 'registro.asesoria.calendario':
                        if 'tripulante_usuario' in values:
                            registros_s_ = odoo_s.execute('res.users', 'read', values['tripulante_usuario'][0][2])
                            logins = []
                            for registro_login in registros_s_:
                                logins.append(registro_login['login'])
                            if len(registros_s_) > 0:
                                id_l_l = odoo_user.env['res.users'].search([('login','in',logins)])
                                values['tripulante_usuario'] = [[6,False,id_l_l]]
                                values_transaccion_s = {'values_transaccion':values}
                                cedula_l = odoo_s.execute('provene.transaccion.bd', 'write', value.id, values_transaccion_s)
                        modelo_l = modelo_l.search([('name','=',cedula_s[0]['name']),('tipo_actividad','=',cedula_s[0]['tipo_actividad'])])
                        registro_modelo = cedula_s[0]['name']
            
            
            
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

                    if len(modelo_l) > 0:
                        for id_l in modelo_l:
                            cedula_l = odoo_user.execute(modelo, 'write', id_l, values)
                            list_.append('Se modificó el registro %s la tabla << %s >> con el metodo %s' % (registro_modelo,modelo,metodo))
                    else:
                        list_.append('No se puedo modificar el registro %s en la tabla << %s >> para poder aplicar el método %s' % (registro_modelo,modelo,metodo))
                
                if metodo == 'unlink':
                    modelo_l = odoo_user.env[modelo]
                    if modelo == 'registro.asesoria':
                        modelo_l = modelo_l.search([('cedula','=',values['cedula'].strip())])
                        registro_modelo = values['cedula']
            
                    if modelo == 'registro.asesoria.calendario':
                        modelo_l = modelo_l.search([('name','=',values['name']),('tipo_actividad','=',values['tipo_actividad'])])
                        registro_modelo = values['name']
            
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
            
                    if modelo == 'casos.legal':
                        # 	list_.append('Se modificó el registro %s la tabla << %s >> con el método %s' % (id_l_l,modelo,metodo))
                        modelo_l = modelo_l.search(['&','&',('cedula','=',values['cedula']),('datos_jornada_calendario','=',values['datos_jornada_calendario']),('categoria_area_legal','=',values['categoria_area_legal'])])
                        registro_modelo = values['cedula']
            
                    if len(modelo_l) > 0:
                        for cedula_ in modelo_l:
                            cedula_l = odoo_user.execute(modelo, 'unlink', cedula_)
                            list_.append('Se eliminó el registro %s la tabla << %s >> con el metodo %s' % (registro_modelo,modelo,metodo))
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

    def main(self):
        # self.reenmplazar_password()
        self.sincronizar_transacciones()
        self.actualizar_transaccion_sincronizada()
        self.mostrar_resultados_update()

    name = fields.Char(
        string='Fecha de Sincronización de las Bases de Datos'
    )
    

    resultados_update = fields.Html(string='Resultados de la Sincronización')
    
    # resultados_actualizar = fields.Text(string='Resultados de la Sincronización')
    

    
    
    
    