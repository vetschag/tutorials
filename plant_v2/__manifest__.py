{
    'name': 'Plant Module',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Plant Template Tree Widget',
    'depends': ['base', 'web', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/project_task_views.xml',
        'report/report_action.xml',
        'report/report_template.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'plant_v2/static/src/css/tree_widget.css',
            'plant_v2/static/src/xml/tree_widget.xml',
            'plant_v2/static/src/js/tree_widget.js',
        ],
    },
    'installable': True,
    'application': True,
}
