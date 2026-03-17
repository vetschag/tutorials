{
    'name': 'Health&Safety',

    'depends': [
        'base_setup'
    ],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'reports/hns_lmra_report_template_CSS.xml',
        'reports/hns_lmra_report.xml',
        'views/hns_lmra_view.xml',
        'views/hns_powra_view.xml',
        'views/hns_menu_view.xml',
        
        
    ],
}


