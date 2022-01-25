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
from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    def send_msg(self):
        return {"type": "ir.actions.act_window",
                "name": _("Whatsapp Message"),
                "res_model": "whatsapp.message.controllers",
                "target": "new",
                "view_mode": "form",
                "view_type": "form",
                "context": {"default_user_id": self.id},
                }
