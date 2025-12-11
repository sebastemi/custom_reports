# -*- coding: utf-8 -*-
{
    'name': "Custom Reports",

    'summary': """
        Extended Sale module, for managing customized reports within the company""",

    'description': """
        Extended Sale module, for managing customized reports within the company
    """,

    'author': "Sebastian Osto",
    'website': "http://www.temi.com",
    'category': 'Sales',
    'version': '0.1',

    'depends': ['base','sale','stock','web','purchase'],

    'data': [
        'reports/dispatch_order/header.xml',
        'reports/dispatch_order/main.xml',
        'reports/dispatch_order/footer.xml',
        'reports/dispatch_order/dispatch_order.xml',

        'reports/national_po/header.xml',
        'reports/national_po/main.xml',
        'reports/national_po/footer.xml',
        'reports/national_po/national_po.xml',

        'reports/international_po/header.xml',
        'reports/international_po/main.xml',
        'reports/international_po/footer.xml',
        'reports/international_po/international_po.xml',

        'reports/material_req/header.xml',
        'reports/material_req/main.xml',
        'reports/material_req/footer.xml',
        'reports/material_req/material_req.xml',

        'reports/purchase_req/header.xml',
        'reports/purchase_req/main.xml',
        'reports/purchase_req/footer.xml',
        'reports/purchase_req/purchase_req.xml',

        'reports/delivery_note_wh/header.xml',
        'reports/delivery_note_wh/main.xml',
        'reports/delivery_note_wh/footer.xml',
        'reports/delivery_note_wh/delivery_note_wh.xml',

        'reports/recept_order/header.xml',
        'reports/recept_order/main.xml',
        'reports/recept_order/footer.xml',
        'reports/recept_order/recept_order.xml',


        'views/stock_picking.xml',
        'views/purchase_order.xml',
        'views/requisition.xml',


    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web.report_assets_common': [
            'custom_reports/static/src/css/report_variables.css'
        ]
    }
}
