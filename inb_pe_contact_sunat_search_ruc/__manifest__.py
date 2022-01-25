# -*- coding: utf-8 -*-
##-----------------------------------------------------------------------------##
#
#    Copyright (C) 2021-TODAY Inbrasol.
#    Author      :  Inbrasol S.A.C.
#    WebSite     : https://www.inbrasol.pe
#
#    This program is copyright property of the author mentioned above.
#    You can"t redistribute it and/or modify it.
#
##-----------------------------------------------------------------------------##
{
    "name": "Contact: Search from SUNAT and RENIEC",
    "version": "14.0.0",
    "summary": "Get information of client from SUNAT or RENIEC",
    "description": "Obtain customer information from SUNAT with RUC or RENIEC with DNI",
    "author": "Inbrasol Perú",
    "maintainer": "Inbrasol Odoo Team",
    "website": "http://www.inbrasol.pe",
    "license": "GPL-3",
    "category": "Customizations",
    "depends": ["base", "contacts", "l10n_latam_base", "l10n_pe"],
    "data": [
        "views/res_partner_view.xml",
        "views/res_company_views.xml",
    ],
    "images": ["/static/description/icon.png"],
    "installable": True,
    "application": False,
    "auto_install": False,
}
