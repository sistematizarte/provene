# -*- coding: utf-8 -*-
{
    'name': "Provene mas datos del Tripulante",

    'summary': """Manage trainings""",

    'description': """
        Open Academy module for managing trainings:
            - training courses
            - training sessions
            - attendees registration
    """,

    'author': "Raymond Sanchez",
    'website': "http://www.sistematizarte.com",

    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'mas_datos_tripulante_view.xml',
    ],
}
