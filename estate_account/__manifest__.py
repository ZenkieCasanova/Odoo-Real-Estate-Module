# -*- coding: utf-8 -*-
{
'name': "Estate Application",
'description': """
 Odoo Developer Technical Exercises of Odoo documentation """,
'author': "Mark Renzkie C. Culambot",
'version': '1.1',
'depends': ['estate','account'],
'data': [
    'security/rules.xml',
    'views/estate_property_views.xml',
    'report/estate_account_report_template.xml',
    'report/estate_account_reports.xml',
],
'sequence': 1,
'installable': True,
'application': True
}
