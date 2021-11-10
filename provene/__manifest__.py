# -*- coding: utf-8 -*-
{
    'name': "provene",

    'summary': """Manage trainings""",

    'description': """
        Open Academy module for managing trainings:
            - training courses
            - training sessions
            - attendees registration
    """,

    'author': "Edgar Melo",
    'website': "http://www.sistematizarte.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','provene_mas_datos_tripulante','board'],

    'qweb': ['static/src/xml/qweb.xml'],
    # always loaded
    'data': [
        'calendar_asesoria_view.xml',
        'registro_area_social.xml',
        'dashboard_cuestionario_inicial.xml',
        'provene_casos_legal_view.xml',        
        'configuracion_view.xml',
        'pagina_inicio.xml',        
        'report.xml',
        'report_bitacora.xml',
        'report_caso_legal.xml',
        'report_casos_atendidos.xml',
        'report_lista_pasajero.xml',
        'report_tripulante.xml',
        'report_tripulante_bitacora.xml',
        'transaccion_view.xml',
        'provene_view.xml'
    ],
}
