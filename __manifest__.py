# -*- coding: utf-8 -*-
{
    'name': "VideoClub",

    'summary': """
       gestinar peliculas""",

    'description': """
        este modulo permitirá gestionar el stock de peliculas de un videoclub , así como los prestamos realizados sobre ellas
    """,

    'author': "a20josefs",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration','Inventory'
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
