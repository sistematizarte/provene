 # -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import models, fields, api
from bs4 import BeautifulSoup
from odoo.exceptions import ValidationError,UserError
import requests
import psycopg2
import pytz
import logging

_logger = logging.getLogger(__name__)

class RegistroAsesoriaLegal(models.Model): 
    _name = 'registro.asesoria'

    
    LIMPIAR_NA_ES_MU = True

    # cuestionario legal on_change

    @api.onchange('cle_activar')
    def on_change_cle_activar(self):
        self.cl1_servicio = False  #({'cl1_servicio': '',})
        self.cl2_canalizar = False #({'cl2_canalizar': '',})
        self.cl3_solicitar = False #({'cl3_solicitar': '',})
        self.cl4_asistencia = False #({'cl4_asistencia': '',})
        self.cl5_tramite = False    #({'cl5_tramite': '',})
        self.cl6_tribunales = False #({'cl6_tribunales': '',})
        self.cl7_experiencia = False #({'cl7_experiencia': '',})
        self.cl8_ddhh = False #({'cl8_ddhh': '',})
        self.cl9_justicia = False #({'cl9_justicia': '',})
        self.cl10_transicional = False  #({'cl10_transicional': '',})

    @api.onchange('cl6_tribunales')
    def on_change_cl6_tribunales(self):
        self.cl7_experiencia = False #({'cl7_experiencia': '',})


    # cuestionario social on_change

    @api.onchange('cso_activar')
    def on_change_cso_activar(self):
        self.cs1_actividad  = False #({'cs1_actividad':'',})
        self.cs3_capacidad = False #({'cs3_capacidad':'',})
        self.cs5_contribuir = False #({'cs5_contribuir':'',})
        self.cs7_participar_actividades = False #({'cs7_participar_actividades':'',})
        self.cs9_expectativas = [(5,)]   

    #limpia campo many2many [(5,0)]
    @api.onchange('cs1_actividad')
    def on_change_cs1_actividad(self):
        self.cs2_actividad_asistencia = [(5,)]

    @api.onchange('cs3_capacidad')
    def on_change_cs3_capacidad(self):
        self.cs4_tribunales = [(5,)]

    @api.onchange('cs5_contribuir')
    def on_change_cs5_contribuir(self):
        self.cs6_no_contribuir = [(5,)]

    @api.onchange('cs7_participar_actividades')
    def on_change_cs7_participar_actividades(self):
        self.cs8_ayuda_economica_exterior  = False #({'cs8_ayuda_economica_exterior': '',})


    # cuestionario inicial on_change     
    @api.onchange('c9_no_responde')
    def on_change_c9_no_responde(self):
        self.c9_personas_viven_usted = False #({'c9_personas_viven_usted': '', })
        self.c10_personas_menores_6 = False #({'c10_personas_menores_6': '', })
        if self.c9_personas_viven_usted:
            self.c9_personas_viven_usted = False #({'c9_personas_viven_usted': '', })
            self.c10_personas_menores_6 = False #({'c10_personas_menores_6': '', })

    @api.onchange('c10_no_responde')
    def on_change_c10_no_responde(self):
        self.c10_personas_menores_6 = False #({'c10_personas_menores_6': '', })
        if self.c10_personas_menores_6:
            self.c10_personas_menores_6 = False #({'c10_personas_menores_6': '', })

    # @api.onchange('c9_no_responde')
    # def on_change_c9_no_responde(self):
    #     self.write({'c9_personas_viven_usted': '', })
    #     self.write({'c10_personas_menores_6': '', })

    # @api.onchange('c10_no_responde')
    # def on_change_c10_no_responde(self):
    #     self.write({'c10_personas_menores_6': '', })

    @api.onchange('c11_no_responde')
    def on_change_c11_no_responde(self):
        self.c11_personas_menores_6_12= False #({'c11_personas_menores_6_12': '', })

    @api.onchange('c14_no_responde')
    def on_change_c14_no_responde(self):
        self.c14_personas_ingresos = False #({'c14_personas_ingresos': '', })
       

    @api.onchange('c11_personas_menores_6_12')
    def on_change_c11_personas_menores_6_12(self):
        self.update({'c12_personas_menores_6_12_escuela': 'pme3', 'c13_frecuencia_escuela': False,})

    @api.onchange('c12_personas_menores_6_12_escuela')
    def on_change_c12_personas_menores_6_12_escuela(self):
        self.c13_frecuencia_escuela = False #({'c13_frecuencia_escuela': '', })

    @api.onchange('c14_personas_ingresos')
    def on_change_c14_personas_ingresos(self):
        self.update({'c15_ingreso_hogar': 'ih2', 'c16_principal_hogar': False,})

    @api.onchange('c15_ingreso_hogar')
    def on_change_c15_ingreso_hogar(self):
        self.c16_principal_hogar = False #({'c16_principal_hogar': '', })

    # registro pasajero on_change

    @api.onchange('imagen')
    def computar_foto(self):
        if self.imagen:
            self.foto_carnet_clave = self.imagen #({'foto_carnet_clave':})

    @api.onchange('nacionalidad_real')
    def generar_cedula_ficticia(self):
        if self.nacionalidad_real == 's':
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)  
            context_today = pytz.utc.localize(fields.Datetime.now()).astimezone(user_tz)
            self.cedula = context_today.strftime("%d%m%Y%H%M%S")
            # self.cedula = fields.Datetime.today().strftime('%Y%m%d%H%M%S%f')
        else:
            self.cedula = False

    @api.onchange('nacionalidad')
    def on_change_pais(self):
        if self.LIMPIAR_NA_ES_MU and self.cedula:
            self.estado = False 
            self.municipio = False 
            self.parroquia = False 
            # ({'estado':False,'municipio':False,'parroquia':False,})

    @api.onchange('estado')
    def on_change_estado(self):
        # _logger.info('onchange(estado)........................................................................... 3 lipoar: %s cedula: %s' % (self.LIMPIAR_NA_ES_MU, self.cedula))
        if self.LIMPIAR_NA_ES_MU and self.cedula:
            self.municipio = False 
            self.parroquia = False
            # self.update({'municipio':False,'parroquia':False,})

    @api.onchange('municipio')
    def on_change_municipio(self):
        if self.LIMPIAR_NA_ES_MU and self.cedula:
            self.parroquia = False
            # self.update({'parroquia':False,})

    @api.onchange('cedula')
    def compute_field(self):

        if self.cedula:
            self.update({
                'nombre': '',
                'apellido': '',
                'telefono_habitacion': '',
                'genero': '',
                'fecha_nacimiento': '',
                'estado_civil': '',
                'direccion': '',
                'nacionalidad':238,
                'estado': self.estado_jornada_hoy,
                'municipio' : self.municipio_jornada_hoy,
                'parroquia': self.parroquia_jornada_hoy,
                'calle_callejon_av_trs' : '',
                'casa_edif' : '',
                'escalera' : '',
                'piso' : '',
                'apartamento' : '',
                'barrio_urb_zona' : '',
                'telefono_celular' : '',
                'telefono_trabajo' : '',
                'hora_contacto' : '',
            })  
            try:
                numero = self.cedula
                # conexion = psycopg2.connect(host="localhost", database="provene", user="openpg", password="openpgpwd")
                # conexion = psycopg2.connect(host="34.66.223.14", database="bitnami_odoo", user="bn_odoo", password="7f30978214")
                # conexion = psycopg2.connect(host="34.66.223.14", database="bitnami_odoo", user="postgres",password="gmWC3QAUudPC")
                # cur = conexion.cursor()
                cur = self.env.cr
                cur.execute(""" SELECT p.cedula, 
                                       concat(COALESCE(primer_nombre,nombre),' ',segundo_nombre) as nombre_completo, 
	                                    concat(COALESCE(primer_apellido,apellido),' ',segundo_apellido) as apellido_completo,
                                        telefono_celular, 
                                        genero, 
                                        fecha_nacimiento, 
                                        estado_civil, 
                                        COALESCE(c.nacionalidad,238) AS pais, 
                                        estado, 
                                        municipio, 
                                        parroquia, 
                                        direccion,
                                        calle_callejon_av_trs,
                                        casa_edif,
                                        escalera,
                                        piso,
                                        apartamento,
                                        barrio_urb_zona,
                                        telefono_habitacion,
                                        telefono_trabajo,
                                        hora_contacto
                                FROM cedulas_venezuela_2012 p LEFT JOIN registro_asesoria c ON p.cedula= cast(c.cedula as int8) 
                                WHERE p.cedula =""" + numero + """ 
                                ORDER BY c.write_date desc 
                                limit 1
                            """)
                if cur.rowcount > 0:
                    self.cedula_existe = True
                    for cedulas_venezuela_2012_registro_asesoria in cur.fetchall():
                        if cedulas_venezuela_2012_registro_asesoria[8]:
                            self.update({'nombre': cedulas_venezuela_2012_registro_asesoria[1],
                                        'apellido': cedulas_venezuela_2012_registro_asesoria[2],
                                        'telefono_celular': cedulas_venezuela_2012_registro_asesoria[3],
                                        'genero': cedulas_venezuela_2012_registro_asesoria[4],
                                        'fecha_nacimiento': cedulas_venezuela_2012_registro_asesoria[5],
                                        'estado_civil': cedulas_venezuela_2012_registro_asesoria[6],
                                        'nacionalidad': cedulas_venezuela_2012_registro_asesoria[7],
                                        'estado': cedulas_venezuela_2012_registro_asesoria[8],
                                        'municipio': cedulas_venezuela_2012_registro_asesoria[9],
                                        'parroquia': cedulas_venezuela_2012_registro_asesoria[10],
                                        'direccion': cedulas_venezuela_2012_registro_asesoria[11],
                                        'calle_callejon_av_trs' : cedulas_venezuela_2012_registro_asesoria[12],
                                        'casa_edif' : cedulas_venezuela_2012_registro_asesoria[13],
                                        'escalera' : cedulas_venezuela_2012_registro_asesoria[14],
                                        'piso' : cedulas_venezuela_2012_registro_asesoria[15],
                                        'apartamento' : cedulas_venezuela_2012_registro_asesoria[16],
                                        'barrio_urb_zona' : cedulas_venezuela_2012_registro_asesoria[17],
                                        'telefono_habitacion' : cedulas_venezuela_2012_registro_asesoria[18],
                                        'telefono_trabajo' : cedulas_venezuela_2012_registro_asesoria[19],
                                        'hora_contacto' : cedulas_venezuela_2012_registro_asesoria[20]
                                        })
                            return{'warning':{'title':'Buscar cédula para el nuevo Pasajero',
                                      'message':'El Pasajero ya se encuentra registrado en la Nave',
                                      'type':'notification'}}
                        else:
                            self.update({'nombre': cedulas_venezuela_2012_registro_asesoria[1],
                                        'apellido': cedulas_venezuela_2012_registro_asesoria[2],
                                        'telefono_celular': cedulas_venezuela_2012_registro_asesoria[3],
                                        'genero': cedulas_venezuela_2012_registro_asesoria[4],
                                        'fecha_nacimiento': cedulas_venezuela_2012_registro_asesoria[5],
                                        'estado_civil': cedulas_venezuela_2012_registro_asesoria[6],
                                        'nacionalidad': cedulas_venezuela_2012_registro_asesoria[7],
                                        'estado': self.estado_jornada_hoy,
                                        'municipio': self.municipio_jornada_hoy,
                                        'parroquia': self.parroquia_jornada_hoy,
                                        'direccion': cedulas_venezuela_2012_registro_asesoria[11],
                                        'calle_callejon_av_trs' : cedulas_venezuela_2012_registro_asesoria[12],
                                        'casa_edif' : cedulas_venezuela_2012_registro_asesoria[13],
                                        'escalera' : cedulas_venezuela_2012_registro_asesoria[14],
                                        'piso' : cedulas_venezuela_2012_registro_asesoria[15],
                                        'apartamento' : cedulas_venezuela_2012_registro_asesoria[16],
                                        'barrio_urb_zona' : cedulas_venezuela_2012_registro_asesoria[17],
                                        'telefono_habitacion' : cedulas_venezuela_2012_registro_asesoria[18],
                                        'telefono_trabajo' : cedulas_venezuela_2012_registro_asesoria[19],
                                        'hora_contacto' : cedulas_venezuela_2012_registro_asesoria[20]
                                        })
                        self.LIMPIAR_NA_ES_MU = False
                else:
                    self.cedula_existe = False
                    self.LIMPIAR_NA_ES_MU = True              
                    
                    return{'warning':{'title':'Buscar cédula para el nuevo Pasajero',
                                      'message':'Debe registrar el Nombre y Apellido del pasajero',
                                      'type':'notification'}}
                # conexion.close()    
            except (Exception, psycopg2.DatabaseError) as error:
                return{'warning':{'title':'Buscar cédula para el nuevo Pasajero',
                                   'message':'Error: %s' %(error)}}
                # conexion.close()    


    @api.depends('fecha_nacimiento')
    def computar_edad_2(self):
        for rec in self:
            if rec.fecha_nacimiento:              
                edad_ext = (fields.Date.from_string(fields.datetime.now().strftime("%Y-%m-%d")) - rec.fecha_nacimiento).days / 365.2425
                rec.edad_ = int(edad_ext)
            else:
                rec.edad_ = 0

    @api.model
    def default_get(self,fields_list):
        res = super(RegistroAsesoriaLegal,self).default_get(fields_list)

        try:
            users_id = str(self.env.uid)       
            # conexion = psycopg2.connect(host="34.66.223.14", database="bitnami_odoo", user="postgres",password="gmWC3QAUudPC")
            # cur = conexion.cursor()
            cur = self.env.cr
            cur.execute( "SELECT name,nacionalidad,estado,municipio,parroquia FROM res_users_registro_asesoria_calendario_rel AS rur, res_users AS ru, registro_asesoria_calendario AS rac WHERE rur.registro_asesoria_calendario_id = rac.id AND rur.res_users_id = ru.id AND rac.fecha_inicio_jornada::date <= now()::date    AND rac.fecha_fin_jornada::date >= now()::date AND rur.res_users_id =" + users_id + " LIMIT 1")
            if cur.rowcount > 0:
                for lugar_jornada in cur.fetchall():
                    res.update({'datos_jornada_calendario':lugar_jornada[0],
                                'nacionalidad':lugar_jornada[1],
                                'estado':lugar_jornada[2],
                                'estado_jornada_hoy':lugar_jornada[2],
                                'municipio':lugar_jornada[3],
                                'municipio_jornada_hoy':lugar_jornada[3],
                                'parroquia':lugar_jornada[4],
                                'parroquia_jornada_hoy':lugar_jornada[4],
                                'nacionalidad_real':'v',
                                })
                    _logger.info('........................................................................... 1.1 %s ' % (lugar_jornada))
            else:
                _logger.info('........................................................................... 2 %s ' % (cur.rowcount))
        except (Exception, psycopg2.DatabaseError) as error:
            print('')
            _logger.info('........................................................................... 3 Error: %s ' % (error))
        # finally:
        #     conexion.close()
            
        cur = self.env.cr
        sql =   """ SELECT count(registro_cuestionario1_c19_id) as veces, registro_cuestionario1_c19_id as rec, 'registro_cuestionario1_c19' as tabla, 'cont_c19' as campo
                    FROM registro_asesoria_registro_cuestionario1_c19_rel
                    group by registro_cuestionario1_c19_id
                    UNION
                    SELECT count(registro_cuestionario1_c21_id) as veces, registro_cuestionario1_c21_id as rec, 'registro_cuestionario1_c21' as tabla, 'cont_c21' as campo
                    FROM registro_asesoria_registro_cuestionario1_c21_rel
                    group by registro_cuestionario1_c21_id
                    UNION
                    SELECT count(registro_cs2_id) as veces, registro_cs2_id as rec, 'registro_cs2' as tabla, 'cont_cs2' as campo
                    FROM registro_asesoria_registro_cs2_rel
                    group by registro_cs2_id
                    UNION
                    SELECT count(registro_cs4_id) as veces, registro_cs4_id as rec, 'registro_cs4' as tabla, 'cont_cs4' as campo
                    FROM registro_asesoria_registro_cs4_rel
                    group by registro_cs4_id
                    UNION
                    SELECT count(registro_cs6_id) as veces, registro_cs6_id as rec, 'registro_cs6' as tabla, 'cont_cs6' as campo
                    FROM registro_asesoria_registro_cs6_rel
                    group by registro_cs6_id
                    UNION
                    SELECT count(registro_cs9_id) as veces, registro_cs9_id as rec, 'registro_cs9' as tabla, 'cont_cs9' as campo
                    FROM registro_asesoria_registro_cs9_rel
                    group by registro_cs9_id
                    ORDER BY tabla, REC
                """
        cur.execute(sql)
        if cur.rowcount > 0:
            _logger.info('........................................................................... 1: %s ' % (cur.statusmessage))
            
            for cuestionario in cur.fetchall():
                sql = "UPDATE %s SET %s=\'%s\' WHERE id=\'%s\'" %(cuestionario[2],cuestionario[3],cuestionario[0],cuestionario[1])
                _logger.info('........................................................................... 2: %s ' % (sql))
                
                cur.execute(sql)
                _logger.info('........................................................................... 3: %s ' % (cur.statusmessage))
                
        return res

    @api.model
    def create(self, values):
        numero = str(values['cedula'])
        cur = self.env.cr
        if len(numero)>6 and values['nacionalidad_real'] != 's' and values['cedula_existe'] == False:
            sql = """       INSERT INTO cedulas_venezuela_2012
                                (nacionalidad
                                ,cedula
                                ,primer_nombre
                                ,primer_apellido
                                ,cod_centro)
                            VALUES
                                (\'%s\',\'%s\',\'%s\',\'%s\',%s)
                        """ %(values['nacionalidad_real'],numero,values['nombre'],values['apellido'], '9999999')
            # raise UserError('valores del SQL que va a insertar %s' %(sql))
            cur.execute(sql)
            _logger.info('entre en create RegistroAsesoriaLegal-----------------------------------------  \t\t\t\t %s \t\t\t\t %s' % (sql,cur.statusmessage))
            
        # else:
            # if len(numero)<=6:
                # raise UserError('No parece ser una cédula válida ---%s --- %s --- %s' %(numero,len(numero),len(numero) <= 6))
                # raise UserError('No parece ser una cédula válida. C.I.: %s' %(numero))
            
        _logger.info('entre en create RegistroAsesoriaLegal********************************************************* 100000 \t\t\t\t %s \t\t\t\t ' % (values))
        values['solo_lectura'] = True
        user = super(RegistroAsesoriaLegal, self).create(values)
        self.guardar_transaccion('create',values,user.id)
        return user

    def write(self, values):
        res = {}
        _logger.info('entre en write RegistroAsesoriaLegal********************************************************* 200000 \t\t\t\t %s \t\t\t\t \t\t\t\t %s \t\t\t\t ' % (self,values))
        if 'cedula' in values:
            _logger.info('entre en write RegistroAsesoriaLegal values[cedula]:********************************************************* 600000 \t\t\t\t %s \t\t\t\t \t\t\t\t %s \t\t\t\t ' % (self,'cedula' in values))
            raise UserError('No se pueden guardar los cambios debido a que ha modificado el número de cédula')
        else:
            res = super(RegistroAsesoriaLegal, self).write(values)
            self.guardar_transaccion('write',values,self.id)
        return res
    
    def unlink(self):
        for id_r in self:
            self.guardar_transaccion('unlink',{'cedula':str(id_r.cedula)},id_r.id)
        return super(RegistroAsesoriaLegal, self).unlink()
    
    
    def guardar_transaccion(self, metodo, values, registro_id):
        datos = {
            # 'name':str(fields.Datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
            'name':str(pytz.utc.localize(fields.Datetime.now()).astimezone(pytz.timezone(self.env.context.get('tz') or self.env.user.tz)).strftime("%d/%m/%Y %H:%M:%S")),
            'modelo_transaccion':'registro.asesoria',
            'metodo_transaccion':metodo,
            'registro_id':registro_id,
            'values_transaccion':values,
            'transaccion_sincronizada':False,
            'values_transaccion_backup':values
        }
        _logger.info('Datos de la Transaccion RegistroAsesoriaLegal********************************************************* 400000 \t\t\t\t %s \t\t\t\t ' % (datos))
        self.env['provene.transaccion.bd'].create(datos)

    #carga la fecha del dia para mostrarla en el footer de los reportes
    @api.model
    def dia_imp(self):
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)  
        context_today = pytz.utc.localize(fields.Datetime.now()).astimezone(user_tz)
        self.fecha_reporte = context_today.strftime("%Y-%m-%d")
    
    #concatena nombre y apellido  lo asigna en rec_name 
    def name_get(self):
        result = []
        for object in self:
            result.append((object.id,object.nombre+' '+object.apellido+' '+object.cedula))
        return result
    
    # Encabezado de la hoja
    titulo_jornada = fields.Char(string='Nombre de la Jornada:', default="Nombre de la Jornada: ",store=False, readonly = True)
    datos_jornada_calendario = fields.Char(string='Nombre de la Jornada', required = True, readonly = True, store=True)

    # Campos comunes
    nombre = fields.Char(string='Nombres',  required = True)
    apellido = fields.Char(string='Apellidos', required = True)
    #foto_carnet = fields.Binary(string='Foto', attachment=True)
    imagen = fields.Binary(string='Foto', attachment=True)
    foto_carnet_clave = fields.Text(string='Referencia Foto')

    # Datos Basicos
    nacionalidad_real = fields.Selection([('v', 'V'),('e', 'E'),('s', 'S/C')], string='Nacionalidad',required = True)
    cedula = fields.Char(string='Cédula',  size=14, help = 'Ingrese solo numeros', required = True,  index = True)
    cedula_existe = fields.Boolean(string='Cédula existe',store=False)
    solo_lectura = fields.Boolean()
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento', required = True)
    # edad = fields.Integer(string='Edad', store=False, readonly = True)
    edad_ = fields.Integer(string='Edad', store=False, readonly = True, compute = 'computar_edad_2')
    email = fields.Char(string='Correo Electrónico')
    genero = fields.Selection([('h', 'Hombre'), ('m', 'Mujer'),('o', 'Otro')], string='Sexo', required = True)
    estado_civil =  fields.Selection([('so', 'Soltero'),('ca', 'Casado/en pareja'),('di', 'Divorciado/Separado'),('ot', 'Viudo')], string='Estado Civil',required = True)

    # Dirección:
    nacionalidad = fields.Many2one('res.country', string='Pais', required = True)
    estado = fields.Many2one('res.country.state', string='Estado', domain="[('country_id','=', nacionalidad)]", required = True)
    estado_jornada_hoy = fields.Integer(store=False)
    municipio = fields.Many2one('res.country.state.municipality', string='Municipio', domain="[('state_id', '=', estado)]", required = True)
    municipio_jornada_hoy = fields.Integer(store=False)    
    parroquia = fields.Many2one('res.country.state.municipality.parish', string='Parroquia', domain="[('municipality_id', '=', municipio)]", required = True)
    parroquia_jornada_hoy = fields.Integer(store=False)    
    calle_callejon_av_trs = fields.Char(string='Calle / Callejón / Av. / Trs.', required = True)
    casa_edif = fields.Char(string='N° Casa / Edf.', required = True)
    # edf_resd_bloque = fields.Char(string='Edf. / Resd. / Bloque', required = True)
    escalera = fields.Char(string='Escalera')
    piso = fields.Char(string='Piso')
    apartamento = fields.Char(string='Apartamento')
    barrio_urb_zona = fields.Char(string='Barrio / Urb. / Zona', required = True)
    direccion = fields.Text(string='Referencias')

    # Telefonos:
    telefono_habitacion = fields.Char(string='Teléfono de habitación', size=15)
    telefono_celular = fields.Char(string='Teléfono Celular', size=15)
    telefono_trabajo = fields.Char(string='Teléfono de Sitio de Trabajo', size=15)
    hora_contacto = fields.Selection([('m', 'Mañana'),('t', 'Tarde'),('n','Noche')], string='Hora posible de contacto')    

    # Reportes:
    fecha_reporte = fields.Date(string='Fecha del Reporte', compute='dia_imp', store=False)


    # Cuestionario Inicial
    c4_nexo_familiar = fields.Selection([('nf1', 'Jefe de Familia'), 
                                         ('nf2', 'Esposa (o/Pareja)'), 
                                         ('nf3', 'Hija / Hijo'), 
                                         ('nf4', 'Yerno / Nuera'), 
                                         ('nf5', 'Padre / Madre'), 
                                         ('nf6', 'Suegro / Suegra'), 
                                         ('nf7', 'Hermano / Hermana'), 
                                         ('nf8', 'Tio / Tia'), 
                                         ('nf9', 'Abuelo / Abuela'), 
                                         ('nf10', 'Otro'),
                                         ('nf11', 'No Desea Responder')], string='Nexo con el Jefe de Familia')   
    c4_nexo_familiar_related = fields.Char(string='Nexo con el Jefe de Familia', store=False)
    c5_grado_instruccion = fields.Selection([('gi1', 'No sabe leer ni escribir'), 
                                             ('gi2', 'Solo leer y escribir'), 
                                             ('gi3', 'Primaria incompleta'), 
                                             ('gi4', 'Primaria completa'), 
                                             ('gi5', 'Secundaria incompleta'), 
                                             ('gi6', 'Secundaria completa'), 
                                             ('gi7', 'Técnica incompleta'), 
                                             ('gi8', 'Técnica completa'), 
                                             ('gi9', 'Universitaria incompleta'), 
                                             ('gi10', 'Universitaria completa'), 
                                             ('gi11', 'Postgrado'),
                                             ('gi12', 'No Desea Responder')], string='Grado de Instrucción')
    c5_grado_instruccion_related = fields.Char(string='Grado de Instrucción', store=False)   
    c6_situacion_ocupacion = fields.Selection([('so1', 'Del Hogar'), 
                                               ('so2', 'Estudiante'), 
                                               ('so3', 'Empleado / Trabajador / Obrero medio tiempo'), 
                                               ('so4', 'Empleado / Trabajador / Obrero tiempo completo'), 
                                               ('so5', 'Trabaja por su cuenta'), 
                                               ('so6', 'Desempleado'), 
                                               ('so7', 'Buscando trabajo por 1ra vez'), 
                                               ('so8', 'Retirado / Jubilado'), 
                                               ('so9', 'No hace nada'), 
                                               ('so10', 'Otro'),
                                               ('so11', 'No Desea Responder')], string='Su Situación de Ocupación')
    c6_situacion_ocupacion_related = fields.Char(string='Su Situación de Ocupación', store=False) 
    c7_tipo_vivienda = fields.Selection([('tipv1', 'Casa'), 
                                         ('tipv2', 'Apartamento'), 
                                         ('tipv3', 'Anexo'), 
                                         ('tipv4', 'Habitación'), 
                                         ('tipv5', 'Otro'),
                                         ('tipv6', 'No Desea Responder')], string='Tipo de Vivienda')
    c7_tipo_vivienda_related = fields.Char(string='Tipo de Vivienda', store=False) 
    c8_tenencia_vivienda = fields.Selection([('tenv1', 'Propia pagada'), 
                                             ('tenv2', 'Propia pagándola'), 
                                             ('tenv3', 'Alquilada'), 
                                             ('tenv4', 'Prestada / Cedida'), 
                                             ('tenv5', 'Otro'),
                                             ('tenv6', 'No Desea Responder')], string='Tenencia de Vivienda')
    c8_tenencia_vivienda_related = fields.Char(string='Tenencia de Vivienda', store=False) 
    c9_personas_viven_usted = fields.Char(string='Número de personas que viven con usted') #mas de 'uno' siga c10 si es '0' siga c11
    c10_personas_menores_6 =fields.Char(string='¿Cuántos son niños menores de 6 años?') 
    c11_personas_menores_6_12 =fields.Char(string='¿Cuántos son niños de 6 a 12 años?')  #mas de 'uno' siga c12 si es '0' siga c14
    c12_personas_menores_6_12_escuela = fields.Selection([('pme1', 'Si, todos'),       #siga c13
                                                          ('pme2', 'Si, algunos'),   #siga c13
                                                          ('pme3', 'Ninguno'),
                                                          ('pme4', 'No Desea Responder')], string='¿Esos niños de 6 a 12 años van a la escuela?', default='pme3') #siga c14
    c12_personas_menores_6_12_escuela_related = fields.Char(string='¿Esos niños de 6 a 12 años van a la escuela?', store=False) 
    c13_frecuencia_escuela = fields.Selection([('fe1', 'Siempre'), 
                                               ('fe2', 'Casi Siempre'), 
                                               ('fe3', 'Pocas Veces'),
                                               ('fe4', 'No Desea Responder')], string='¿Con qué frecuencia van los niños a la escuela?')
    c13_frecuencia_escuela_related = fields.Char(string='¿Con qué frecuencia van los niños a la escuela?', store=False) 
    c14_personas_ingresos =fields.Char(string='¿Cuántas personas perciben algún ingreso en su hogar?')  #mas de 'uno' siga c15 si es '0' siga c17
    c15_ingreso_hogar = fields.Selection([('ih1', 'Si'),                        #siga c16
                                          ('ih2', 'No'),
                                          ('ih3', 'No Desea Responder')], string='¿Es usted alguna de esas personas que reciben algún ingreso en su hogar?' , default='ih2')   #siga c17
    c15_ingreso_hogar_related = fields.Char(string='¿Es usted alguna de esas personas que reciben algún ingreso en su hogar?', store=False) 
    c16_principal_hogar = fields.Selection([('ph1', 'Si'),  
                                            ('ph2', 'No'),
                                            ('ph3', 'No Desea Responder')], string='¿Es usted el sustento principal del hogar?')
    c16_principal_hogar_related = fields.Char(string='¿Es usted el sustento principal del hogar?', store=False) 
    c17_familia_exterior = fields.Selection([('fh1', 'Si'), 
                                             ('fh2', 'No'),
                                             ('fh3', 'No Desea Responder')], string='¿Tiene usted o alguna otra persona de su hogar familiares directos en el exterior?')
    c17_familia_exterior_related = fields.Char(string='¿Tiene usted o alguna otra persona de su hogar familiares directos en el exterior?', store=False) 
    c18_ayuda_economica_exterior = fields.Selection([('aee1', 'Si'), 
                                                     ('aee2', 'No'),
                                                     ('aee3', 'No Desea Responder')], string='¿Recibe usted  o alguna otra persona de su hogar ayuda económica desde el exterior?')
    c18_ayuda_economica_exterior_related = fields.Char(string='¿Recibe usted  o alguna otra persona de su hogar ayuda económica desde el exterior?', store=False) 
    c19_beneficios_estado = fields.Many2many('registro.cuestionario1.c19', 'registro_asesoria_registro_cuestionario1_c19_rel',  string='¿Reciben en su hogar o usted directamente alguno de los siguientes beneficios o ayuda social?')
    c19_beneficios_estado_related = fields.Char(string='¿Reciben en su hogar o usted directamente alguno de los siguientes beneficios o ayuda social?', store=False, related='c19_beneficios_estado.c19_beneficios_estado')
    c20_comidas_diarias = fields.Selection([('cd1', 'Siempre'), 
                                            ('cd2', 'Casi Siempre'), 
                                            ('cd3', 'Algunas Veces'), 
                                            ('cd4', 'Muy rara vez'),
                                            ('cd5', 'No Desea Responder')], string='¿Hacen las tres comidas al día en su casa?')
    c20_comidas_diarias_related = fields.Char(string='¿Hacen las tres comidas al día en su casa?', store=False) 
    c21_principal_problema = fields.Many2many('registro.cuestionario1.c21', 'registro_asesoria_registro_cuestionario1_c21_rel', string='¿Cuáles considera usted que son los tres principales problemas que usted enfrenta actualmente?')
    c21_principal_problema_related = fields.Char(string='¿Cuáles considera usted que son los tres principales problemas que usted enfrenta actualmente?', store=False, related='c21_principal_problema.c21_principal_problema')
    c22_referido = fields.Selection([('ref1', 'Vecino / Amigo'), 
                                ('ref2', 'Publicidad en la Comunidad'), 
                                ('ref3', 'Redes Sociales'),
                                ('ref4', 'Por Acercarse al Truck'),  
                                ('ref5', 'Otros'),
                                ('ref6', 'No Desea Responder')], string='Referido por:')
    c22_referido_related = fields.Char(string='Referido por:', store=False) 

    c9_no_responde = fields.Boolean(string = 'No Desea Responder')
    c10_no_responde = fields.Boolean(string = 'No Desea Responder')
    c11_no_responde = fields.Boolean(string = 'No Desea Responder')
    c14_no_responde = fields.Boolean(string = 'No Desea Responder')

    cle_activar = fields.Boolean(string = 'Cuestionario Legal')
    cso_activar = fields.Boolean(string = 'Cuestionario Social')

    # Cuestionario Legal
    cl1_servicio =  fields.Selection([('ser1', 'Si'),
                                       ('ser2', 'No'),
                                       ('ser3', 'No Desea Responder')], string='¿Ha utilizado alguna vez algún servicio de PROVENE?')
    cl1_servicio_related = fields.Char(string='¿Ha utilizado alguna vez algún servicio de PROVENE?', store=False) 

    cl2_canalizar =  fields.Selection([('can1', 'Si'),
                                     ('can2', 'No'),
                                     ('can3', 'No Desea Responder')], string='¿Ha tenido alguna vez algún caso legal que no haya podido canalizar?')
    cl2_canalizar_related = fields.Char(string='¿Ha tenido alguna vez algún caso legal que no haya podido canalizar?', store=False) 

    cl3_solicitar = fields.Selection([('sol1', 'Si'),
                                      ('sol2', 'No'),
                                      ('sol3', 'No Desea Responder')], string='¿Está aquí para solicitar algún trámite legal o asistencia jurídica?')
    cl3_solicitar_related = fields.Char(string='¿Está aquí para solicitar algún trámite legal o asistencia jurídica?', store=False) 

    cl4_asistencia =  fields.Selection([('asi1', 'Si'),
                                       ('asi2', 'No'),
                                       ('asi3', 'No Desea Responder')], string='¿Es la primera vez que busca este tipo de asistencia?')
    cl4_asistencia_related = fields.Char(string='¿Es la primera vez que busca este tipo de asistencia?', store=False) 

    cl5_tramite =  fields.Selection([('tram1', 'Personal'),
                                    ('tram2', 'Familiar'),
                                    ('tram3', 'No Desea Responder')], string='¿Qué tipo de trámite necesitaría? ')
    cl5_tramite_related = fields.Char(string='¿Qué tipo de trámite necesitaría?', store=False) 

    cl6_tribunales = fields.Selection([('tri1', 'Si'),
                                      ('tri2', 'No'),
                                      ('tri3', 'No Desea Responder')], string='¿Ha ido usted previamente a los tribunales a resolver asuntos legales?')
    cl6_tribunales_related = fields.Char(string='¿Ha ido usted previamente a los tribunales a resolver asuntos legales?', store=False) 

    cl7_experiencia = fields.Selection([('exp1', 'Muy Buena'), 
                                       ('exp2', 'Buena'), 
                                       ('exp3', 'Regular'), 
                                       ('exp4', 'Mala'), 
                                       ('exp5', 'Muy Mala'),
                                       ('exp6', 'No Desea Responder')], string='¿Cómo ha sido tu experiencia?')
    cl7_experiencia_related = fields.Char(string='¿Cómo ha sido tu experiencia?', store=False) 

    cl8_ddhh = fields.Selection([('ddhh1', 'Si'), 
                                       ('ddhh2', 'No sé'), 
                                       ('ddhh3', 'No'),
                                       ('ddhh4', 'No Desea Responder')], string='¿Considera usted que en Venezuela se violan los DDHH?')
    cl8_ddhh_related = fields.Char(string='¿Considera usted que en Venezuela se violan los DDHH?', store=False) 

    cl9_justicia = fields.Selection([('jus1', 'Si'),
                                      ('jus2', 'No sé'), 
                                      ('jus3', 'No'),
                                      ('jus4', 'No Desea Responder')], string='¿Considera usted que en Venezuela hay justicia?')
    cl9_justicia_related = fields.Char(string='¿Considera usted que en Venezuela hay justicia?', store=False) 

    cl10_transicional = fields.Selection([('trans1', 'Si'),
                                          ('trans2', 'No'),
                                          ('trans3', 'No Desea Responder')], string='¿Sabe usted qué es la Justicia Transicional?')
    cl10_transicional_related = fields.Char(string='¿Sabe usted qué es la Justicia Transicional?', store=False) 



    #  Cuestionario Social
    cs1_actividad = fields.Selection([('act1', 'Si'), 
                                      ('act2', 'No'),
                                      ('act3', 'No Desea Responder')], string='¿Ha participado usted en alguna actividad o taller de carácter social, tal como Taller de arte, Cine foro, Danza, Teatro social, Música o de algún otro tipo?')
    cs1_actividad_related = fields.Char(string='¿Ha participado usted en alguna actividad o taller de carácter social, tal como Taller de arte, Cine foro, Danza, Teatro social, Música o de algún otro tipo?', store=False) 
    
    cs2_actividad_asistencia = fields.Many2many('registro.cs2', 'registro_asesoria_registro_cs2_rel',  string='¿A cuál taller o actividad ha asistido? ')
    cs2_actividad_asistencia_related = fields.Char(string='¿A cuál taller o actividad ha asistido? ', store=False, related='cs2_actividad_asistencia.cs2_actividad_asistencia')

    cs3_capacidad =  fields.Selection([('cap1', 'Si, seguro'),
                                       ('cap2', 'No sé, puede ser'), 
                                       ('cap3', 'No'),
                                       ('cap4', 'No Desea Responder')], string='¿Se siente usted en la capacidad de mejorar su vida y la de su familia?')
    cs3_capacidad_related = fields.Char(string='¿Se siente usted en la capacidad de mejorar su vida y la de su familia?', store=False) 
    
    cs4_tribunales =fields.Many2many('registro.cs4', 'registro_asesoria_registro_cs4_rel', string='¿Qué le hace sentir que usted no es capaz de mejorar su vida o la de su familia?')
    cs4_tribunales_related = fields.Char(string='¿Qué le hace sentir que usted no es capaz de mejorar su vida o la de su familia?', store=False, related='cs4_tribunales.cs4_tribunales')

    cs5_contribuir = fields.Selection([('con1', 'Si, seguro'),
                                       ('con2', 'No sé, puede ser'), 
                                       ('con3', 'No'),
                                       ('con4', 'No Desea Responder')], string='¿Le gustaría a usted, estaría dispuesto a contribuir con su comunidad, mejorar su comunidad?')
    cs5_contribuir_related = fields.Char(string='¿Le gustaría a usted, estaría dispuesto a contribuir con su comunidad, mejorar su comunidad?', store=False) 
    
    cs6_no_contribuir =fields.Many2many('registro.cs6', 'registro_asesoria_registro_cs6_rel', string='¿Qué le hace no estar dispuesto a mejorar ni contribuir con su comunidad?')
    cs6_no_contribuir_related = fields.Char(string='¿Qué le hace no estar dispuesto a mejorar ni contribuir con su comunidad?', store=False, related='cs6_no_contribuir.cs6_no_contribuir')

    cs7_participar_actividades = fields.Selection([('pact1', 'Si, seguro'), 
                                                   ('pact2', 'No sé, puede ser'),
                                                   ('pact3', 'No'),
                                                   ('pact4', 'No Desea Responder')], string='¿Le gustaría a usted, estaría  dispuesto a participar en las actividades sociales que propone La Nave?')
    cs7_participar_actividades_related = fields.Char(string='¿Le gustaría a usted, estaría  dispuesto a participar en las actividades sociales que propone La Nave?', store=False) 
    
    cs8_ayuda_economica_exterior = fields.Text(string='¿Por qué no sabes o no estarías dispuesto a participar en La Nave?')
    
    cs9_expectativas = fields.Many2many('registro.cs9', 'registro_asesoria_registro_cs9_rel', string=' ¿Cuáles son sus expectativas por participar en alguna de las actividades de La Nave? ¿Qué esperas de esa participación?')
    cs9_expectativas_related = fields.Char(string='¿Cuáles son sus expectativas por participar en alguna de las actividades de La Nave? ¿Qué esperas de esa participación?', store=False, related='cs9_expectativas.cs9_expectativas')
