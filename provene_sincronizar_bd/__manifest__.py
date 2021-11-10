# -*- coding: utf-8 -*-
{
    'name': "Sincronización entre las Bases de Datos de Provene",

    'summary': """Manage trainings""",

    'description': """
        Este módulo permite sincronizar todas las Bases de Datos de la Nave de ProVene:
            - La que esta alojada en la nuve.
            - Con la que esta en cada uno de los camiones.
    """,

    'author': "Raymond Sanchez",
    'website': "http://www.sistematizarte.com",

    'category': 'Bases de Datos',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'sincronizar_view.xml',
        # 'transaccion_view.xml',
        'credenciales_view.xml',
    ],
}
