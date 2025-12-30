# -*- coding: utf-8 -*-
{
    'name': "Portal Workflow",
    'sequence': 0,
    'summary': """""",

    'description': """
        Ce module introduit de nouveaux champs dans le modèle res.partner, customization de nouveaux rapports""",

    'author': "FINOUTSOURCE",
    'website': "",

    'category': 'AL SALAM BANK / Portal Workflow',
    'version': '0.1',

    'depends': ['base', 'website', 'crm', 'dept_wk', 'auth_signup'],
    'images': ['/portal_salam/static/description/logo.png'],  # For banners

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/error_page.xml',
        'views/portail_page.xml',
        'views/lead_inherit.xml',
        'views/links.xml',
        'views/website_footer.xml',
        'views/website_navbar.xml',
        'views/website_login.xml',
        'data/cron.xml',
        'views/menu.xml',
        'views/page_not_found.xml',

    ],

    'assets': {
        'web.assets_frontend': [
            'portal_salam/static/src/js/steps_components/partners.js',
            'portal_salam/static/src/js/steps_components/managementTeam.js',
            'portal_salam/static/src/js/steps_components/financialRequests.js',
            'portal_salam/static/src/js/steps_components/situation.js',
            'portal_salam/static/src/js/steps_components/suppliers.js',
            'portal_salam/static/src/js/steps_components/clients.js',
            'portal_salam/static/src/js/steps_components/companies.js',
            'portal_salam/static/src/js/steps/form1.js',
            'portal_salam/static/src/js/steps/form2.js',
            'portal_salam/static/src/js/steps/form3.js',
            'portal_salam/static/src/js/steps/form4.js',
            'portal_salam/static/src/js/steps/form5.js',
            'portal_salam/static/src/js/steps/form6.js',
            'portal_salam/static/src/js/steps_components/stepsIndicatorControl.js',
            'portal_salam/static/src/js/steps_components/stepsIndicator.js',
            'portal_salam/static/src/js/form.js',
            'portal_salam/static/src/js/login.js',
            'portal_salam/static/src/css/style.css',


        ],
        'web.assets_backend': [
            'portal_salam/static/src/css/style.css',]
    },
    'application': True,
    'license': 'LGPL-3',
}
