# -*- coding: utf-8 -*-
{
    'name': "elgam3ia_mgt",
    'summary': """   elgam3ia_mgt """,
    'description': """elgam3ia_mgt\n
    
    """,
    'author': "Awd Sultan",
    'website': "#",
    'category': 'uncategorized',
    'version': '15',
    'depends': ['base','mail','hr','account'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/cycle.xml',
        'views/menus.xml',
        'views/account_payment.xml',
        'views/account_invoice.xml',
    ],
    'demo': [
    ],
}
