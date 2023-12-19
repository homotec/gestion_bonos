# -*- coding: utf-8 -*-
{
    'name': 'Gestion simple de Bonos',
    'version': '1.0.1',
    'summary': 'Gestion Bonos',
    'sequence': 15,
    'website': 'https://www.homotec.com',
    'price': 15,
    'currency': 'EUR',
    "license": "LGPL-3",
    'author': 'Lorenzo Bauza Fischer',
    'description': """Permite llevar una gestion simple de bonos sin vincular con pedidos.""",
    'category': 'General',
    'depends': ['base','product'],
    'data': [
        'views/gestion_bonos_view.xml',
        'views/gestion_bonos_menu.xml',
        'security/security.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
