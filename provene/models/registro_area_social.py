# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import models, fields, api
import psycopg2
import pytz
import logging

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class RegistroActividadSocial(models.Model):
    
    _name = "registro.actividad.social"
    _rec_name = 'actividad_area_social'
    
    @api.model
    def create(self, values):
        _logger.info('entre en create RegistroActividadSocial********************************************************* 700000 \t\t\t\t %s \t\t\t\t ' % (values))
        
        user = super(RegistroActividadSocial, self).create(values)
        
        return user
    
    #carga la fecha del dia para mostrarla en el footer de los reportes
    @api.onchange('tipo_actividad_2')
    def dia_imp(self):
        self.actividad_area_social = ""
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)  
        context_today = pytz.utc.localize(fields.Datetime.now()).astimezone(user_tz)
        self.fecha_inicio_actividad = context_today.strftime("%Y-%m-%d")


    actividad_area_social = fields.Many2one('registro.asesoria.calendario', string='Actividad', domain="[('fecha_inicio_jornada', '>=', fecha_inicio_actividad),('tipo_actividad','=', tipo_actividad_2)]", required = True)
    fecha_inicio_actividad = fields.Datetime(string='Fecha de Inicio',  store=False)
    fecha_inicio_bitacora=fields.Datetime(string='Fecha de Inicio bitacora')
    tipo_actividad_2 = fields.Selection([('tiac1', 'Integral'),
                                       ('tiac3', 'Artística'), 
                                       ('tiac4', 'Fisica'), 
                                       ('tiac5', 'Emocional'), 
                                       ('tiac6', 'Emprendimiento')], string='Tipos de Actividad', store=True)
    pasajeros_id = fields.One2many('registro.pasajeros.actividad.social', 'actividad_id', 'Pasajeros Convocados')

class RegistroPasajerosActividadSocial(models.Model):
    
    _name = "registro.pasajeros.actividad.social"
    _rec_name = 'nombre'

    @api.model
    def create(self, values):
        values['solo_lectura'] = True
        user = super(RegistroPasajerosActividadSocial, self).create(values)
        self.guardar_transaccion('create',values,user.id)
        
        return user

    def write(self, values):
        res = {}
        if 'cedula' in values or 'actividad_id' in values :
            raise UserError('No se pueden guardar los cambios debido a que ha modificado el número de cédula')
        else:
            res = super(RegistroPasajerosActividadSocial, self).write(values)
            self.guardar_transaccion('write',values,self.id)
        return res

    def unlink(self):
        for id_r in self:
            self.guardar_transaccion('unlink',{'cedula':str(id_r.cedula),'actividad_id':str(id_r.actividad_id.id)},id_r.id)
        return super(RegistroPasajerosActividadSocial, self).unlink()


    def guardar_transaccion(self, metodo, values, registro_id):
        datos = {
            # 'name':str(fields.Datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
            'name':str(pytz.utc.localize(fields.Datetime.now()).astimezone(pytz.timezone(self.env.context.get('tz') or self.env.user.tz)).strftime("%d/%m/%Y %H:%M:%S")),
            'modelo_transaccion':'registro.pasajeros.actividad.social',
            'metodo_transaccion':metodo,
            'registro_id':registro_id,
            'values_transaccion':values,
            'transaccion_sincronizada':False,
            'values_transaccion_backup':values
        }
        # _logger.info('Datos de la Transaccion RegistroAsesoriaLegal********************************************************* 400000 \t\t\t\t %s \t\t\t\t ' % (datos))
        self.env['provene.transaccion.bd'].create(datos)
        
    #carga por defecto los estados en la vista kanban
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).estatus_convocatoria.selection]


    #cargando datos del pasajero registrado con el numero de cedula
    @api.onchange('cedula')
    def compute_field(self):
        self.update({'nombre': '', 'apellido': '',  })
        if self.cedula:    
            try:
                numero = self.cedula
                # conexion = psycopg2.connect(host="34.66.223.14", database="bitnami_odoo", user="postgres",password="gmWC3QAUudPC")
                # cur = conexion.cursor()
                cur = self.env.cr
                cur.execute( "SELECT nombre, apellido FROM registro_asesoria WHERE cedula ='" + numero + "' limit 1")
                if cur.rowcount > 0:
                    for nombre_completo, apellido_completo  in cur.fetchall():
                        self.update({'nombre': nombre_completo,'apellido': apellido_completo})
                else:
                    return{'warning':{'title':'Buscando Datos del Pasajero','message':'Esta persona no es miembro de la Nave.', 'type':'notification'}}
            except (Exception, psycopg2.DatabaseError) as error:
                return{'warning':{'title':'Buscando Datos del Pasajero','message':'Error: %s' %(error)}}
            # finally:
                # conexion.close()

        else:
            self.update({'nombre': '', 'apellido': '',  })


    #carga la fecha del dia para mostrarla en el footer de los reportes
    @api.onchange('tipo_actividad_3')
    def dia_imp(self):
        self.actividad_id = ""
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)  
        context_today = pytz.utc.localize(fields.Datetime.now()).astimezone(user_tz)
        # self.write({'fecha_inicio_actividad': context_today.strftime("%d/%m/%Y %H:%m:%s")}) 
        self.fecha_inicio_actividad = context_today.strftime("%Y-%m-%d")


    actividad_id = fields.Many2one('registro.actividad.social', string = 'Actividad', domain="[('fecha_inicio_bitacora', '>=', fecha_inicio_actividad),('tipo_actividad_2','=', tipo_actividad_3)]", required = True)
    
    fecha_inicio_actividad = fields.Datetime(string='Fecha de Inicio',  store=False)
    tipo_actividad_3 = fields.Selection([('tiac1', 'Integral'),
                                       ('tiac3', 'Artística'), 
                                       ('tiac4', 'Fisica'), 
                                       ('tiac5', 'Emocional'), 
                                       ('tiac6', 'Emprendimiento')], string='Tipos de Actividad', store=True)

    # Encabezado de la hoja
    estatus_convocatoria = fields.Selection([('nasis', 'No Asistió'), ('conv', 'Convocado'), ('asis', 'Asistió')], string='Convocatoria', default='conv',  group_expand='_expand_states')

    # Campos comunes
    cedula = fields.Char(string='Cédula', required = True,  size=8, help = 'Ingrese solo numeros')
    nombre = fields.Char(string='Nombres',required = True )
    apellido = fields.Char(string='Apellidos',required = True )
    
    #Campo de apollo
    solo_lectura = fields.Boolean()
    


class valorCs02(models.Model):

    _name = "registro.cs2"
    _rec_name = 'cs2_actividad_asistencia'

    cs2_actividad_asistencia = fields.Char(string='¿A cuál taller o actividad ha asistido?')
    cont_cs2 = fields.Integer(string='Cantidad Respuesta')

class valorCs04(models.Model):

    _name = "registro.cs4"
    _rec_name = 'cs4_tribunales'
    cs4_tribunales = fields.Char(string='¿Qué le hace sentir que usted no es capaz de mejorar su vida o la de su familia?')
    cont_cs4 = fields.Integer(string='Cantidad Respuesta')

class valorCs06(models.Model):

    _name = "registro.cs6"
    _rec_name = 'cs6_no_contribuir'
    cs6_no_contribuir = fields.Char(string='¿Qué le hace no estar dispuesto a mejorar ni contribuir con su comunidad?')
    cont_cs6 = fields.Integer(string='Cantidad Respuesta')

class valorCs09(models.Model):

    _name = "registro.cs9"
    _rec_name = 'cs9_expectativas'
    cs9_expectativas = fields.Char(string='¿Cuáles son sus expectativas por participar en alguna de las actividades de La Nave? ¿Qué esperas de esa participación?')
    cont_cs9 = fields.Integer(string='Cantidad Respuesta')

class valorC19(models.Model):

    _name = "registro.cuestionario1.c19"
    _rec_name = 'c19_beneficios_estado'
    c19_beneficios_estado = fields.Char(string='¿Reciben en su hogar o usted directamente alguno de los siguientes beneficios o ayuda social?')
    cont_c19 = fields.Integer(string='Cantidad Respuesta')

class valorC21(models.Model):

    _name = "registro.cuestionario1.c21"
    _rec_name = 'c21_principal_problema'
    c21_principal_problema = fields.Char(string='¿Cuáles considera usted que son los tres principales problemas que usted enfrenta actualmente?')
    cont_c21 = fields.Integer(string='Cantidad Respuesta')