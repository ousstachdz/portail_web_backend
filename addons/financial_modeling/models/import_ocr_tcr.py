
from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
import re    
import base64
import pytesseract
from pdf2image import convert_from_bytes
import tempfile
import numpy as np
import cv2
from difflib import SequenceMatcher
class ImportTcrOCR(models.Model):
    _name = 'import.ocr.tcr'
    _description = "Import Tcr Data by OCR Functionality"

    name = fields.Char(string="Réf")
    date = fields.Date(string="Date d'importation", default=datetime.today())
    annee = fields.Char(string="Année de l'exercice")
    company = fields.Char(string="Désignation de l'entreprise")
    tcr_lines = fields.One2many("import.ocr.tcr.line", "tcr_id", string="Lignes", domain=lambda self: self._get_domain())
    file_import = fields.Binary(string="Import de fichier")
    file_import2 = fields.Binary(string="Import de fichier")
    file_import_name = fields.Char(string="Fichier")
    hide_others = fields.Boolean(string="Filter que les lignes concernées")
    state = fields.Selection([("get_data", "Import données"),
                              ("validation", "Validation"),
                              ("valide", "Validé"),
                              ('modified', 'Modifié par le risque')], string="Etat", default="get_data")

    def _get_domain(self):
        if self.hide_others:
            return [('sequence', 'in', [7, 33, 50, 36, 12, 13, 14, 30])]
        else:
            []

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('import.ocr.tcr.seq')
        return super(ImportTcrOCR, self).create(vals)

    def open_file(self):
        for rec in self:
            view_id = self.env.ref('financial_modeling.extract_bilan_wizard_form').id
            context = dict(self.env.context or {})
            context['pdf_1'] = rec.file_import
            context['pdf_2'] = rec.file_import2
            context['tcr_id'] = rec.id
            wizard = self.env['extract.bilan.wizard'].create({'pdf_1': rec.file_import,
                                                              'pdf_2': rec.file_import2,})
            return {
                'name': 'TCR',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'extract.bilan.wizard',
                'res_id': wizard.id,
                'view_id': view_id,
                'target': 'new',
                'context': context,
            }
  
    def extract_data(self):
        def process_file(file_data, record_id):
            """Processes a file (file_import or file_import2) for OCR extraction."""
            if not file_data:
                return

            data = str(file_data)
            data = data.replace("b'", '\n').replace("'", '')
            data = data.replace('\r\n', '\n').replace('\r', '\n')
            data = 'data:application/pdf;base64,' + data

            # Retrieve all configurations
            configs = self.env['import.ocr.config'].search([('type', '=', 'tcr')])
            items = [config.name for config in configs]

            # Perform OCR
            ocr_results = get_text_from_pdf_base64(pdf_base64=data, items=items)
            if ocr_results:
                for result in ocr_results:
                    config_match = next((config for config in configs if config.name == result['name']), None)
                    if config_match:
                        self.env['import.ocr.tcr.line'].create({
                            'tcr_id': record_id,
                            'name': result['name'],
                            'rubrique': config_match.id,
                            'montant_n': result['number_1'],
                            'montant_n1': result['number_2']
                        })

        for record in self:
            if record.file_import:
                if record.tcr_lines:
                    record.tcr_lines.unlink()

                process_file(record.file_import, record.id)

            if record.file_import2:
                process_file(record.file_import2, record.id)

            record.state = "validation"

    def action_validation(self):
        for rec in self:
            list_validation = [7, 12, 13, 14, 33, 50, 42]
            tcr = rec.tcr_lines.filtered(lambda r: r.rubrique.sequence in list_validation)
            if len(tcr) != 7:
                raise ValidationError("Vous devriez confirmer les valeurs suivantes: \n "
                                      "- Chiffre d'affaires net des rabais, Remises, Ristournes \n"
                                      "- Achats de marchandises vendues \n"
                                      "- Matières premieres \n"
                                      "- Autres approvisionnements \n"
                                      "- Excédent brut de l'exploitation \n"
                                      "- Charges financières \n"
                                      "- Résultat  net de l'exercice")
            view_id = self.env.ref('financial_modeling.confirmation_wizard_form')
            context = dict(self.env.context or {})
            context['tcr_id'] = rec.id
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
            context['tcr_id'] = rec.id
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


class ImportTcrOcrLine(models.Model):
    _name = "import.ocr.tcr.line"
    _description = "Line de tcr importé"

    name = fields.Char(string="RUBRIQUES")
    sequence = fields.Integer(related='rubrique.sequence')
    mintop = fields.Integer(string='Rang')
    height = fields.Integer(string='Height')
    montant_n = fields.Float(string="N")
    montant_n1 = fields.Float(string="N-1")
    rubrique = fields.Many2one('import.ocr.config', string='Rubriques confirmés', domain="[('type','=','tcr')]")
    tcr_id = fields.Many2one('import.ocr.tcr', string="TCR ID")


class ConfigRubrique(models.Model):
    _name = 'import.ocr.config'
    _description = 'Liste des rubriques'

    name = fields.Char(string='rubrique')
    type = fields.Selection([('tcr', 'TCR'),
                             ('actif', 'Actif'),
                             ('passif', 'Passif')], string='Type')
    sequence = fields.Integer(string="Sequence")
    




def extract_table_from_image(image):
    """Extracts a table from an image using OCR."""
    try:
        img = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        custom_config = (
            r'-c preserve_interword_spaces=1x1 --dpi 300 --psm 1 --oem 3 '
            r'preserve_interword_spaces=1 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz'
            r'ABCDEFGHIJKLMNOPQRSTUVWXYZéèàôâê '
        )
        raw_text = pytesseract.image_to_string(img, config=custom_config)
        raw_text = re.sub(r'\s{2,}', '\n', raw_text)  # Normalize whitespace
        rows = raw_text.split("\n")
        matrix = [row.split("\t") for row in rows if row.strip()]
        return matrix
    except Exception as e:
        raise ValidationError(f"Error during table extraction: {e}")



def get_text_from_pdf_base64(pdf_base64, items):
    """Processes a base64 PDF to extract OCR text."""
    try:
        if pdf_base64.startswith("data:application/pdf;base64,"):
            pdf_base64 = pdf_base64.split(",")[1]

        pdf_data = base64.b64decode(pdf_base64)

        with tempfile.TemporaryDirectory() as temp_dir:
            images = convert_from_bytes(pdf_data, output_folder=temp_dir)
            result_matrix = []
            for image in images:
                page_matrix = extract_table_from_image(image)
                result_matrix.extend(page_matrix)  # Combine matrices from all pages

            return handle_values_ocr(result_matrix, items)
    except Exception as e:
        raise ValidationError(f"Error during PDF processing: {e}")
    
def handle_values_ocr(result_matrix,items):
    print("############################ Matrix Item vs Item ############################")
    match_counter = 0
    item_object_list = []
    for item in items:
            for matrix_item in result_matrix:
                item_cleaned = re.sub(r'[^a-zA-Z0-9]', '', item)
                item_cleaned = item_cleaned.replace("I", "l")
                matrex_cleaned = matrix_item[0].replace("I", "l")
                
                item_cleaned = item_cleaned.replace("1", "l")
                matrex_cleaned = matrex_cleaned.replace("1", "l")
                
                item_cleaned = item_cleaned.replace("in", "21332132321")
                matrex_cleaned = matrex_cleaned.replace("in", "21332132321")
                item_cleaned = item_cleaned.replace("ô", "o")
                matrex_cleaned = matrex_cleaned.replace("ô", "o")
    for matrix_item in result_matrix:
        similarity_table=[]
        for item in items:
            similarity_table.append({"item":item ,"sim":SequenceMatcher(a=matrix_item[0], b=item.strip()).ratio()})
        similarity = max(similarity_table, key=lambda x: x.get("sim", 0))   
        if similarity['sim'] > 0.65:
            match_counter += 1
            current_index = result_matrix.index(matrix_item)
            item_object = {
                    'name': similarity['item'],
                    'number_1': int(re.sub(r'[^0-9]', '', result_matrix[current_index + 1][0])) if re.search(r'\d', result_matrix[current_index + 1][0]) else 0,
                    'number_2': int(re.sub(r'[^0-9]', '', result_matrix[current_index + 2][0])) if re.search(r'\d', result_matrix[current_index + 2][0]) and re.search(r'\d', result_matrix[current_index + 1][0]) else 0
                }
            item_object_list.append(item_object)

    return item_object_list