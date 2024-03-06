
{
    'name': 'Custom DMS Validation',
    'summary': """Custom DMS Validation""",
    'version': '16.0.1.0.0',
    'description': """Custom DMS Validation""",
    'author': 'Flowdoo',
    'company': 'Flowdoo',
    'website': 'https://flowdoo.co',
    'category': 'Tools',
    'depends': ['base','dms','base_tier_validation'],
    'license': 'AGPL-3',
    'data': [
        'views/dms_file_view.xml',
        'views/dms_directory_view.xml',
    ],
    'installable': True,
}

