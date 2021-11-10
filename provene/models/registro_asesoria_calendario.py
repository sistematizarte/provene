from odoo import models, fields, api
import logging
import psycopg2
import pytz
from odoo.exceptions import ValidationError,UserError


_logger = logging.getLogger(__name__)

class CalendarioAsesoriaLegal(models.Model):

	_name = 'registro.asesoria.calendario'


	 #tcarga la fecha del dia para mostrarla en el footer de los reportes
	@api.model
	def dia_imp(self):
	    user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)  
	    context_today = pytz.utc.localize(fields.Datetime.now()).astimezone(user_tz)
	    self.fecha_reporte = context_today.strftime("%Y-%m-%d")

	@api.model
	def create(self, values):
		values['solo_lectura'] = True
		user = super(CalendarioAsesoriaLegal, self).create(values)
		if values['tipo_actividad'] != 'tiac2':
			values_ = {'actividad_area_social': user.id,
					   'tipo_actividad_2': values['tipo_actividad'],
					   'fecha_inicio_bitacora': values['fecha_inicio_jornada']}
			self.env['registro.actividad.social'].create(values_)
   
		self.guardar_transaccion('create',values,user.id)
		
		return user

	def write(self, values):
		if 'name' in values or 'tipo_actividad' in values:
			_logger.info('entre en write RegistroAsesoriaLegal values[name]:********************************************************* 600000 \t\t\t\t %s \t\t\t\t \t\t\t\t %s \t\t\t\t ' % (self,'cedula' in values))
			raise UserError('No se pueden guardar los cambios debido a que ha modificado el nombre o el tipo de la actividad')
		else:
			res = super(CalendarioAsesoriaLegal, self).write(values)
			if self.tipo_actividad != 'tiac2':
				res_actividad_social = self.env['registro.actividad.social'].search([('actividad_area_social', '=', self.id)])
				if res_actividad_social:
					values_ = {
						'tipo_actividad_2': self.tipo_actividad,
						'fecha_inicio_bitacora': self.fecha_inicio_jornada}
					res_actividad_social.write(values_)
				else:
					values_ = {'actividad_area_social': self.id,
						'tipo_actividad_2': self.tipo_actividad,
						'fecha_inicio_bitacora': self.fecha_inicio_jornada}
					self.env['registro.actividad.social'].create(values_)
			else:
				self.env['registro.actividad.social'].search([('actividad_area_social', '=', self.id)]).unlink()
			
			self.guardar_transaccion('write',values,self.id)

		return res

	def unlink(self):
		user = {}
		
		for ras in self:
			res_actividad_social = self.env['registro.actividad.social'].search([('actividad_area_social', '=', ras.id)]) 
			res_actividad_social.unlink()

		for id_r in self:
			self.guardar_transaccion('unlink',{'name':str(id_r.name),'tipo_actividad':str(id_r.tipo_actividad)},id_r.id)
   
		user = super(CalendarioAsesoriaLegal, self).unlink()
		return user

	def guardar_transaccion(self, metodo, values, registro_id):
		datos = {
			'name':str(pytz.utc.localize(fields.Datetime.now()).astimezone(pytz.timezone(self.env.context.get('tz') or self.env.user.tz)).strftime("%d/%m/%Y %H:%M:%S")),
			'modelo_transaccion':'registro.asesoria.calendario',
			'metodo_transaccion':metodo,
			'registro_id':registro_id,
			'values_transaccion':values,
			'transaccion_sincronizada':False,
			'values_transaccion_backup':values
		}
		_logger.info('Datos de la Transaccion CalendarioAsesoriaLegal********************************************************* 400000 \t\t\t\t %s \t\t\t\t ' % (datos))
		self.env['provene.transaccion.bd'].create(datos)
  
	### Carga en la tabla registro_cuestionario_social los pasajeros convocados a las actividades activas del dia
	 
	name = fields.Char(string='Nombre de la Actividad',  required = True)
	descripcion_jornada = fields.Text(string='Descripcion de la Actividad', required = True)
	fecha_inicio_jornada = fields.Datetime(string='Fecha de Inicio', required = True)
	fecha_fin_jornada = fields.Datetime(string='Fecha de Culminacion',  required = True)
	parroquia = fields.Many2one('res.country.state.municipality.parish', string='Parroquia', domain="[('municipality_id', '=', municipio)]", required = True)
	municipio = fields.Many2one('res.country.state.municipality', string='Municipio', domain="[('state_id', '=', estado)]", required = True)
	estado = fields.Many2one('res.country.state', string='Estado', domain="[('country_id', '=', nacionalidad)]", required = True)
	nacionalidad = fields.Many2one('res.country', string='Nacionalidad', default =238, required = True)
	direccion = fields.Text(string='Dirección',required = True)
	separator_campo = fields.Char(string="fila vacia", store =False)
	tripulante_usuario = fields.Many2many('res.users','res_users_registro_asesoria_calendario_rel',  string='Tripulante Asistente', required = True, default=lambda self: self.env.user)
	nombre_tripulante= fields.Many2one('res.users', string = 'Nombre del Tripulante')
	tipo_actividad = fields.Selection([('tiac1', 'Integral'),
		                               ('tiac2', 'Legal'),
		                               ('tiac3', 'Artística'), 
	                                   ('tiac4', 'Fisica'), 
	                                   ('tiac5', 'Emocional'), 
	                                   ('tiac6', 'Emprendimiento')], string='Tipos de Actividad', required = True)

	# Reportes:
	fecha_reporte = fields.Date(string='Fecha del Reporte', compute='dia_imp', store=False)
	
	# Apoyo para Readonly
	solo_lectura = fields.Boolean()
	