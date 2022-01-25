# -*- coding: utf-8 -*-
##-----------------------------------------------------------------------------##
#
#    Copyright (C) 2021-TODAY Inbrasol.
#    Author      : Inbrasol S.A.C.
#    WebSite     : https://www.inbrasol.pe
#
#    This program is copyright property of the author mentioned above.
#    You can"t redistribute it and/or modify it.
#
##-----------------------------------------------------------------------------##
{
    "name": "Contact: Whatsapp Redirect",
    "version": "14.0.0",
    "summary": "Send Message to partner via Whatsapp web",
    "description": "Send Message to partner or client via whatsapp web",
    "author": "Inbrasol Perú",
    "maintainer": "Inbrasol Odoo Team",
    "website": "http://www.inbrasol.pe",
    "license": "GPL-3",
    "category": "Customizations",
    "depends": ["base", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/partner_view.xml",
        "controllers/whatsapp_sendMessage_view.xml",
    ],
    "images": ["/static/description/icon.png"],
    "installable": True,
    "application": False,
    "auto_install": False,
}
