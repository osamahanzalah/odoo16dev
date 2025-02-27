# -*- coding: utf-8 -*-
{
    'name': 'Employee Documents',
    'version': '15.0.1.0.0',
    'summary': """Manages Employee Documents """,
    'description': """""",
    'category': 'hr',
    'author': '',
    'company': '',
    'maintainer': '',
    'website': "",
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_document_type.xml',
        'views/employee_document_view.xml',
        'views/res_config_setting.xml',
        'views/all_documents.xml',
        'views/not_attached_doc.xml',
        'views/expiry_documents.xml',
    ],
    'demo': ['data/data.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
