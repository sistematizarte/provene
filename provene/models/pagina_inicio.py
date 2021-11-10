# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import models, fields, api
import psycopg2

class PaginaInicio(models.Model): 
    _name = 'pagina.inicio'

    def _get_default_pagina(self):
    # 	return """<div style="background: url(/provene/static/description/background_login_1.png) no-repeat center center fixed;
    #    -webkit-background-size: cover;
    # -moz-background-size: cover;
    # -o-background-size: cover;
    # background-size: cover;
    # height: 100%;
    # width: 100% ;
    # text-align: center;
    #     ">

    # </div>"""
        return """    <table>
        <tr>
            <td>
                <img alt="" src="/provene/static/description/INICIO_SISTEMA_LN_FINAL-04.png" style="width: 100%;"/>

            </td>
        </tr>
    </table>"""

    cuadro_1 = fields.Char(string = 'Inicio', default= _get_default_pagina, readonly=True) 

