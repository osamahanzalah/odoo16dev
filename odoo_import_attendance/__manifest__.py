# -*- coding: utf-8 -*-
{
    'name': 'Odoo Import Attendances',
    'summary': "Import Attendances from Excel",
    'description': "General Import Attendances from Excel",
    'author': "Awd",
    'website': "#",
    'category': 'Attendance',
    'version': '15',
    'depends': [
        'hr_attendance','base'
    ],
    'external_dependencies': {
        'python': [
            'xlrd',
            'xlwt',
        ]
    },
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_attendance_view.xml',
        'views/hr_employee.xml',
        'views/attendance_records.xml',
        'views/excel_col.xml',
    ],

    'auto_install': False,
    'installable': True,

}
