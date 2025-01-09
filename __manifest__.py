{
    'name': 'ICS Purchase Order',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Customization module for ICS Group',
    'description': "Customization module purchase order for ICS Group. "
    "This module contains lead time configuration on product category "
    "and Approval function to secure record creating that can configure",
    'author': 'pieceoftech, ICS',
    'website': 'https://ics-seafood.com',
    'license': 'AGPL-3',
    'depends': ['base', 'base_automation', 'product', 'stock', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'data/approval_config.xml',
        'data/approval_mail_template.xml',
        'report/purchase_order_template.xml',
        'report/purchase_order_report.xml',
        'wizard/approval_wizard.xml',
        'views/approval_config.xml',
        'views/lead_time_view.xml',
        'views/product_category.xml',
        'views/purchase_order_view.xml',
        'views/purchase_approval.xml'
    ],
    'installable': True,
}