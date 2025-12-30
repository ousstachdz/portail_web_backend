from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError, UserError
import base64
from io import BytesIO
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
import tempfile

import re
import json
import requests

from .import_ocr_tcr import extract_table_from_image, get_text_from_pdf_base64, handle_values_ocr
class ImportPassifOCR(models.Model):
    _name = "import.ocr.passif"
    _description = "Import Bilan Passif Data by OCR Functionality"

    name = fields.Char(string="Réf")
    date = fields.Date(string="Date d'importation", default=datetime.today())
    annee = fields.Char(string="Année de l'exercice")
    company = fields.Char(string="Désignation de l'entreprise")
    passif_lines = fields.One2many("import.ocr.passif.line", "passif_id", string="Lignes", domain=lambda self: self._get_domain())
    file_import = fields.Binary(string="Import de fichier")
    file_import_name = fields.Char(string="Fichier")
    hide_others = fields.Boolean(string="Filter que les lignes concernées")
    state = fields.Selection([("get_data", "Import données"),
                              ("validation", "Validation"),
                              ("valide", "Validé"),
                              ('modified', 'Modifié par le risque')], string="Etat", default="get_data")

    def _get_domain(self):
        if self.hide_others:
            return [('sequence', 'in', [2, 4, 8, 12, 14, 18, 20, 21, 22, 23, 24, 25])]
        else:
            []

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('import.ocr.passif.seq')
        return super(ImportPassifOCR, self).create(vals)

    def open_file(self):
        for rec in self:
            view_id = self.env.ref('financial_modeling.extract_bilan_wizard_form').id
            context = dict(self.env.context or {})
            context['pdf_1'] = rec.file_import
            context['passif_id'] = rec.id
            wizard = self.env['extract.bilan.wizard'].create({'pdf_1': rec.file_import})
            return {
                'name': 'Passif',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'extract.bilan.wizard',
                'res_id': wizard.id,
                'view_id': view_id,
                'target': 'new',
                'context': context,
            }
    def extract_data(self):
        for rec in self:
            if rec.file_import:
                pattern_alpha = r'^[a-zA-Z\séèàôâê\'();,*+-1]+$'
                pattern_num = r'^[0-9\s()\-]+$'
                if rec.passif_lines:
                    rec.passif_lines.unlink()
                data = str(rec.file_import)
                data = data.replace("b'", '\n')
                data = data.replace("'", '')
                data = data.replace('\r\n', '\n')  # Replace Windows-style newline with Unix-style
                data = data.replace('\r', '\n')
                data = 'data:application/pdf;base64,' + data

                print("step 0")
                all_configues = self.env['import.ocr.config'].search([('type', '=', 'passif')])
                items = [config.name for config in all_configues]
                print("step 1")
                ocr_results = get_text_from_pdf_base64(pdf_base64=data,items=items)
                for result in ocr_results:
                    print("step 2")
                    rubrique = next((config for config in all_configues if config.name == result['name']), None)
                    if rubrique:
                        print("step 3")
                        value = rec.env['import.ocr.passif.line'].create(
                            {
                                'passif_id': rec.id,
                                'name': result['name'],
                                'rubrique': rubrique.id,
                                'montant_n': result['number_1'],
                                'montant_n1': result['number_2']
                            })
                rec.state = "validation"
            else:
                raise UserError('Un probleme est survenu, vous devriez réessayer ulterieurement.')

    def action_validation(self):
        for rec in self:
            list_validation = [12, 14, 20, 23, 24, 25]
            passifs = rec.passif_lines.filtered(lambda r: r.rubrique.sequence in list_validation)
            if len(passifs) != 6:
                raise ValidationError("Vous devriez confirmer les valeurs suivantes: \n"
                                      "- Total I \n"
                                      "- Emprunts et dettes financières \n"
                                      "- Fournisseurs et comptes rattachés \n"
                                      "- Trésorerie passifs \n"
                                      "- Total III \n"
                                      "- Total General Passif (I+II+III)")
            view_id = self.env.ref('financial_modeling.confirmation_wizard_form')
            context = dict(self.env.context or {})
            context['passif_id'] = rec.id
            context['state'] = 'valide'
            print(context)
            if not self._context.get('warning'):
                return {
                    'name': 'Validation',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'import.ocr.wizard',
                    'view_id': view_id.id,
                    'target': 'new',
                    'context': context,
                }

    def action_annulation(self):
        for rec in self:
            view_id = self.env.ref('financial_modeling.confirmation_wizard_form')
            context = dict(self.env.context or {})
            context['passif_id'] = rec.id
            context['state'] = 'validation'
            print(context)
            if not self._context.get('warning'):
                return {
                    'name': 'Annulation',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'import.ocr.wizard',
                    'view_id': view_id.id,
                    'target': 'new',
                    'context': context,
                }
                
    
class ImportPassifOcrLine(models.Model):
    _name = "import.ocr.passif.line"
    _description = "Line de bilan passif importé"

    name = fields.Char(string="RUBRIQUES")
    mintop = fields.Integer(string='Rang')
    height = fields.Integer(string='Height')
    sequence = fields.Integer(related='rubrique.sequence')
    rubrique = fields.Many2one('import.ocr.config', string='Rubriques confirmés', domain="[('type','=','passif')]")
    montant_n = fields.Float(string="N")
    montant_n1 = fields.Float(string="N-1")
    passif_id = fields.Many2one('import.ocr.passif', string="Passif ID")

