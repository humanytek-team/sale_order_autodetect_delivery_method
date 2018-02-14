# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Autodetects delivery method in sale orders',
    'version': '9.0.1.0.7',
    'category': 'Sales',
    'author': 'Humanytek',
    'website': "http://www.humanytek.com",
    'license': 'AGPL-3',
    'depends': ['sale', 'delivery', 'base_partner_delivery_currier'],
    'data': [
        'views/res_company_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
