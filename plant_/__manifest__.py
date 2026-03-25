{
    'name': 'Plant Module',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Plant Template Tree Widget',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'report/report_action.xml',
        'report/report_template.xml',
    ],
    'demo': [
        'demo/demo_data.xml',      # Testdaten — nur im Demo-Modus
    ],
    'assets': {
        'web.assets_backend': [
            'plant/static/src/css/tree_widget.css',
            'plant/static/src/xml/tree_widget.xml',
            'plant/static/src/js/tree_widget.js',
        ],
    },
    'installable': True,
    'application': True,
}
