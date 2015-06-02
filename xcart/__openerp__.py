{
'name': 'X-Cart OpenERP',
'version': '1.0',
'category': 'E-Commerce',
'description': """
This module allows you to connect X-Cart and OpenERP
===============================
""",
'author': 'Ismaylov Rufat',
'depends': ['base','sale'],
'init_xml': ['xcart_menu_view.xml'],
'update_xml':['xcart_menu_view.xml'],
'installable': True,
'auto_install': False,
'active':True
}