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
from odoo import models, api, fields

class WhatsappSendMessage(models.TransientModel):

    _name = "whatsapp.message.controllers"
    _description = "Whatsapp Controller"
    user_id = fields.Many2one("res.partner", string="Recipient")
    mobile = fields.Char(related="user_id.mobile", required=True)
    message = fields.Text(string="message", required=True)

    def send_message(self):
        if self.message and self.mobile:
            message_string = ""
            message = self.message.split(" ")
            for msg in message:
                message_string = message_string + msg + "%20"
            message_string = message_string[:(len(message_string) - 3)]
            return {
                "type": "ir.actions.act_url",
                "url": "https://api.whatsapp.com/send?phone="+self.user_id.mobile+"&text=" + message_string,
                "target": "new",
                "res_id": self.id,
            }
