from odoo import fields,models

class WKEtapeWizard(models.Model):
    _name = 'wk.consulter.compte'
    _description = 'For to display account balance'

    etape_id = fields.Many2one('wk.etape', string="Etape", required=True)
    compte_client_ids = fields.One2many(
        'wk.compte.client', 'etape_id', string="Client Accounts"
    )