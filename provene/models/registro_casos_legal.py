# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import models, fields, api
import psycopg2
import pytz
from odoo.exceptions import UserError



class RegistroCasosLegal(models.Model): 
    _name = 'casos.legal'
    
    @api.model
    def create(self, values):
        values['solo_lectura'] = True
        user = super(RegistroCasosLegal, self).create(values)
        self.guardar_transaccion('create',values,user.id)
        return user

    def write(self, values):
        res = {}
        if 'cedula' in values or 'datos_jornada_calendario' in values or 'categoria_area_legal' in values:
            raise UserError('No se pueden guardar los cambios debido a que ha modificado el número de cédula o el nombre de la actividad o la categoria')
        else:
            res = super(RegistroCasosLegal, self).write(values)
            self.guardar_transaccion('write',values,self.id)
        return res
    
    def unlink(self):
        for id_r in self:
            self.guardar_transaccion('unlink',{'cedula':str(id_r.cedula),'datos_jornada_calendario':str(id_r.datos_jornada_calendario),'categoria_area_legal':str(id_r.categoria_area_legal)},id_r.id)
        return super(RegistroCasosLegal, self).unlink()
    
    
    def guardar_transaccion(self, metodo, values, registro_id):
        datos = {
            # 'name':str(fields.Datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
            'name':str(pytz.utc.localize(fields.Datetime.now()).astimezone(pytz.timezone(self.env.context.get('tz') or self.env.user.tz)).strftime("%d/%m/%Y %H:%M:%S")),
            'modelo_transaccion':'casos.legal',
            'metodo_transaccion':metodo,
            'registro_id':registro_id,
            'values_transaccion':values,
            'transaccion_sincronizada':False,
            'values_transaccion_backup':values
        }
        # _logger.info('Datos de la Transaccion RegistroAsesoriaLegal********************************************************* 400000 \t\t\t\t %s \t\t\t\t ' % (datos))
        self.env['provene.transaccion.bd'].create(datos)


    @api.onchange('categoria_area_legal')
    def on_change_categoria_area_legal(self):
        if self.categoria_area_legal:
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)  
            context_today = pytz.utc.localize(fields.Datetime.now()).astimezone(user_tz)
            self.update({'fecha_documento_entregado' :context_today.strftime("%Y-%m-%d %H:%M:%S")})
            if self.categoria_area_legal =="ase" or self.categoria_area_legal =="con":
                self.update({'estatus' : 'ent'}) 

            else:
                self.update({'estatus' : 'reg'})


    @api.onchange('cedula')
    def compute_field(self):
        self.update({'nombre': '', 'apellido': '',})
        if self.cedula:
            try:
                numero = self.cedula
                # conexion = psycopg2.connect(host="34.66.223.14", database="bitnami_odoo", user="postgres",password="gmWC3QAUudPC")
                # cur = conexion.cursor()
                cur = self.env.cr
                cur.execute( "SELECT nombre, apellido, foto_carnet_clave FROM registro_asesoria WHERE cedula ='" + numero + "' limit 1")
                if cur.rowcount > 0:
                    for nombre_completo, apellido_completo, foto_carnet_clave_referencia  in cur.fetchall():
                        self.update({'nombre': nombre_completo,'apellido': apellido_completo, 'foto':foto_carnet_clave_referencia})
                else:
                    return{'warning':{'title':'Buscar cédula para el nuevo Pasajero','message':'Esta persona no es miembro de la Nave.', 'type':'notification'}}
            except (Exception, psycopg2.DatabaseError) as error:
                return{'warning':{'title':'Buscar cédula para el nuevo Pasajero','message':'Error: %s' %(error)}}
            # finally:
            #     conexion.close()
        
        else:
            self.update({'nombre': '', 'apellido': '',  })

    #carga por defecto los datos de la jornada en el form
    def _get_default_Datos_jornada(self):
        try:
            users_id = str(self.env.uid)
           
            # conexion = psycopg2.connect(host="34.66.223.14", database="bitnami_odoo", user="postgres",password="gmWC3QAUudPC")
            #conexion = psycopg2.connect(host="127.0.0.1", database="bitnami_odoo", user="bn_odoo", password="554153744c")
            # conexion = psycopg2.connect(host="34.66.223.14", database="bitnami_odoo", user="bn_odoo", password="7f30978214")
            # cur = conexion.cursor()
            cur = self.env.cr
            cur.execute( "SELECT name FROM res_users_registro_asesoria_calendario_rel AS rur,res_users AS ru,registro_asesoria_calendario AS rac WHERE rur.registro_asesoria_calendario_id = rac.id   AND rur.res_users_id = ru.id    AND rac.fecha_inicio_jornada::date <= now()::date    AND rac.fecha_fin_jornada::date >= now()::date AND rur.res_users_id =" + users_id + " limit 1")
            if cur.rowcount > 0:
                for nombre_jornada in cur.fetchall():
                    return nombre_jornada[0]
            else:
                return ""
        except:
            return ""
        # finally:
        #     conexion.close()

    #carga por defecto los estados en la vista kanban
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).estatus.selection]    
 
    #carga la fecha del dia para mostrarla en el footer de los reportes
    @api.model
    def dia_imp(self):
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)  
        context_today = pytz.utc.localize(fields.Datetime.now()).astimezone(user_tz)
        self.fecha_reporte = context_today.strftime("%Y-%m-%d")


    # Encabezado de la hoja
    titulo_jornada = fields.Char(string='Nombre de la Jornada:', default="Nombre de la Jornada: ",store=False, readonly = True)
    datos_jornada_calendario = fields.Char(string='Nombre Jornada', default= _get_default_Datos_jornada, required = True, readonly = True, store=True)
    estatus = fields.Selection([('reg', 'Solicitado'), ('ela', 'Emitido'), ('ent', 'Entregado/Resuelto')], string='Estatus', default='reg', group_expand='_expand_states')

    # Campos comunes
    # nacionalidad_real = fields.Selection([('v', 'V'),('e', 'E'),('s', 'S/C')], string='Nacionalidad',required = True)
    cedula = fields.Char(string='Cédula',  size=8, help = 'Ingrese solo numeros', required = True)
    #nombre = fields.Char(string='Nombres',  required = True, readonly = True, store=True)
    nombre = fields.Char(string='Nombres',  required = True)
    #apellido = fields.Char(string='Apellidos', required = True, readonly = True, store=True)
    apellido = fields.Char(string='Apellidos',  required = True)
    foto = fields.Binary(string='Foto')

    # Área Legal
    # Redacción de documentos
    observaciones_caso = fields.Text(string='Observaciones')
    tripulante_asignado = fields.Many2one('res.users', string='Tripulante Asignado',default=lambda self: self.env.user)
    recaudos_recibidos = fields.Selection([('s', 'Si'), 
                              ('n', 'No')], string='Recaudos Recibidos')
    fecha_documento_entregado = fields.Datetime(string='Fecha de Estatus')
    instruccion_caso = fields.Many2many('instruccion.valor', 'casos_legal_instruccion_valor_rel', string='Tipo de Documento')
    tipo_documento = fields.Char(string='Tipo de Documento', store=True, related='instruccion_caso.instruccion_valor')

    # Asesoria
    datos_asesoria= fields.Many2one('asesoria.valor', string='Tipo de Asesoría')
    descripcion_asesoria = fields.Text(string='Descripción')


    # Conciliación
    cedula_parte2 = fields.Char(string='Cédula de la Contraparte',  size=8, help = 'Ingrese sólo números')
    nombre_parte2 = fields.Char(string='Nombre de la Contraparte')
    direccion_parte2 = fields.Text(string='Dirección de la Contraparte') 
    fecha_citacion = fields.Date(string='Fecha de Citación' )

    # Categorias del Área Legal
    categoria_area_legal = fields.Selection([('rdt', 'Redacción de Documentos'),
                                             ('ase', 'Asesoría'), 
                                             ('con', 'Conciliación')], string='Categoria Area Legal', default='rdt',required = True)
    # Fin Área Legal
    
    #Apoyo para convertir en read only
    solo_lectura = fields.Boolean()
    
    # Reportes:
    fecha_reporte = fields.Date(string='Fecha del Reporte', compute='dia_imp', store=False)