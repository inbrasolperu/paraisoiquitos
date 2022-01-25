# -*- coding: utf-8 -*-
##-----------------------------------------------------------------------------##
#
#    Copyright (C) 2021-TODAY Inbrasol.
#    Author      :  Inbrasol S.A.C.
#    WebSite     : https://www.inbrasol.pe
#
#    This program is copyright property of the author mentioned above.
#    You can't redistribute it and/or modify it.
#
##-----------------------------------------------------------------------------##
from requests.models import Response
from odoo import models, fields, api, _
import requests
import json


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _default_country(self):
        return self.env.company.country_id.id

    country_id = fields.Many2one(default=_default_country)
    commercial_name = fields.Char(string="Commercial Name")
    alert_warning_vat = fields.Boolean(string="Alert warning vat", default=False)
    condition = fields.Selection([('habido', 'Habido'), ('nhabido', 'No Habido')], string="condition")
    status = fields.Selection([('activo', 'Activo'), ('stemporal', 'Suspensión temporal'),
                               ('bajaprovicional', 'Baja provisional'), (
                                   'bajadefinitiva', 'Baja definitiva'),
                               ('sbajaprovicionaloficio', 'Baja provisional de oficio'), ('sbajadefinitivaoficio', 'Baja definitiva de oficio')], string="status")

    @api.onchange('vat', 'l10n_latam_identification_type_id')
    def onchange_vat(self):
        res = {}
        if self.vat:
            if self.l10n_latam_identification_type_id.l10n_pe_vat_code == '6':
                if len(self.vat) != 11:
                    res['warning'] = {'title': _('Warning'), 'message': _(
                        'The Ruc must be 11 characters long.')}
                else:
                    company = self.env['res.company'].browse(self.env.company.id)
                    if company.l10n_pe_ruc_validation == True:
                        self.get_data_ruc()
            elif self.l10n_latam_identification_type_id.l10n_pe_vat_code == '1':
                if len(self.vat) != 8:
                    res['warning'] = {'title': _('Warning'), 'message': _(
                        'The Dni must be 8 characters long.')}
                else:
                    company = self.env['res.company'].browse(
                        self.env.company.id)
                    if company.l10n_pe_dni_validation == True:
                        self.get_data_dni()
        if res:
            return res

    def get_data_ruc(self):
        result = self.sunat_connection(self.vat)
        if result:
            self.alert_warning_vat = False
            self.company_type = 'company'
            self.name = str(result['business_name']).strip().upper()
            city = self.env['res.city'].search(
                [('l10n_pe_code', '=', result['city_id'])], limit=1)
            district = self.env['l10n_pe.res.city.district'].search(
                [('code', '=', result['district_id'])], limit=1)
            self.l10n_pe_district = district.id
            self.city_id = city.id
            self.state_id = city.state_id
            self.country_id = city.country_id
            self.street = str(result['street']).strip().title()
            # SET contributing_condition SUNAT
            if result['contributing_condition'] == 'HABIDO':
                self.condition = 'habido'
            else:
                self.condition = 'nhabido'
            # SET contributing_status SUNAT
            if result['contributing_status'] == 'ACTIVO':
                self.status = 'activo'
            elif result['contributing_status'] == 'SUSPENSION TEMPORAL':
                self.status = 'stemporal'
            elif result['contributing_status'] == 'BAJA PROVISIONAL':
                self.status = 'bajaprovicional'
            elif result['contributing_status'] == 'BAJA DEFINITIVA':
                self.status = 'bajadefinitiva'
            elif result['contributing_status'] == 'BAJA PROVISIONAL DE OFICIO':
                self.status = 'bajaprovicionaloficio'
            elif result['contributing_status'] == 'BAJA DEFINITIVA DE OFICIO':
                self.status = 'bajadefinitivaoficio'

    def get_data_dni(self):
        result = self.reniec_connection(self.vat)
        if result:
            self.alert_warning_vat = False
            self.name = str(result['name'] or '').strip().title()
            self.company_type = 'person'

    @api.model
    def sunat_connection(self, ruc):
        session = requests.Session()
        headers = requests.utils.default_headers()
        token = 'apis-token-1039.7EvthKGrxEzS3HxTbUrtfTtJxzkMHMoz'
        headers = {"Authorization":token}
        url="https://api.apis.net.pe/v1/ruc?numero=#ruc#"
        data = {}
        try:
            response = requests.get(url.replace("#ruc#",ruc), headers=headers, timeout=(15))
            if response.status_code == 200:
                result = response.json()
                data['business_name'] = result.get('nombre')
                data['contributing_status'] = result.get('estado')
                data['contributing_condition'] = result.get('condicion')
                data['ubigeo'] = result.get('ubigeo').strip()
                data['state_id'] = data['ubigeo'][0:2]
                data['city_id'] = data['ubigeo'][0:4]
                data['district_id'] = data['ubigeo'][0:6]
                data['street'] = result.get('direccion')
            else:
                self.alert_warning_vat = True
                data = False
                #direccion_completa = result.get('direccion_completa')
                #ultima_actualizacion = result.get('ultima_actualizacion')
        except Exception:
            self.alert_warning_vat = True
            data = False
        return data

    @api.model
    def reniec_connection(self, dni):
        token = 'apis-token-1039.7EvthKGrxEzS3HxTbUrtfTtJxzkMHMoz'
        session = requests.Session()
        headers = requests.utils.default_headers()
        headers = {"Authorization":token}
        url =  'https://api.apis.net.pe/v1/dni?numero=#dni#'
        data = {}
        try:
            response = requests.get(url.replace("#dni#",dni), headers=headers, timeout=(15))
            if response.status_code == 200:
                result = response.json()
                data['name'] = result.get('nombre')
            else:
                self.alert_warning_vat = True
                data = False
        except Exception:
            self.alert_warning_vat = True
            data = False
        return data