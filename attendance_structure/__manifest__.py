# -*- coding: utf-8 -*-
{
    'name': "Attendance Structure",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'hr',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_attendance','om_hr_payroll'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/attendance_rules.xml',
        'views/attendance_structure.xml',
        'views/hr_attendance.xml',
        'views/resource_calendar.xml',
        'views/hr_payslip.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
