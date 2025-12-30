# models/cron_http.py
import requests
from ..__constants__ import BASE_URL, DATABASE, PASSWORD, USERNAME
from odoo import models, _,fields
import logging
from datetime import timedelta
import base64


_logger = logging.getLogger(__name__)


class CronLead(models.Model):
    _name = 'crm.lead.cron'
    _description = 'HTTP Request Cron'

    def send_http_request(self):
        session = requests.Session()
        base_url = BASE_URL


	
        class_b = {
            'demande', 'forme_jur'
        }
        class_c = {
             'apropos', 'gestion', 'tailles',
            'fournisseurs', 'clients', 'situations', 'companies', 'documents'
        }
        ids_recieved = []
        data_a = {}
        data_b = {}
        data_c = {}

        try:
            data_response = session.get(f'{base_url}/opportunity/get_oopportunites', timeout=10, verify=False, )

            data_response.raise_for_status()
            response_json = data_response.json()
            records = response_json.get('opportunities', []) if response_json.get('opportunities') else {}
            for record in records:
                for key, value in record.items():
                    if key == 'id':
                        if value in ids_recieved:
                            _logger.info(f'Record with id {value} already processed, skipping.')
                            continue
                        ids_recieved.append(value)
                    if key in class_b:
                        data_b[key] = value
                    elif key in class_c:
                        data_c[key] = value
                    else:
                        data_a[key] = value

                _logger.info('Record: %s', data_a)
                opportunity = self.env['crm.lead'].sudo().create(data_a)
                _logger.info('Opportunity step 1 created ')


                try:
                    link = self.env['ponctual.links'].sudo().search(
                        [('link_uid', '=', data_a.get('link_hash'))], limit=1)
                    if link:
                        if link.user_id:
                            opportunity.sudo().write({
                                'user_id': link.user_id.id,
                                'branche': link.user_id.branche.id,
                    	    })
                    _logger.info('Opportunity step add agency created ')
                    _logger.info(f'Opportunity step add agency created {link.user_id.name}---{link.user_id.branche.name}----{link.link_uid}----{data_a.get("link_hash")}')
                except Exception as e :
                    _logger.error('Opportunity step add agency not created ')
                    _logger.info('Opportunity step add agency not created ')
                    _logger.error(f'step not created because:{e}')


                try:
                    opportunity.sudo().write({
                        'demande':       data_b.get('demande'),
                        'forme_jur':     data_b.get('forme_jur'),
                    })
                    _logger.info('Opportunity step 2 created ')
                except Exception as e :
                    _logger.error('Opportunity step 2 not created ')
                    _logger.error(f'step not created because:{e}')

                try:
                   
                    partner_ids, gestion_ids, taille_ids, fournisseur_ids, client_ids, situation_ids, company_ids = [
                    ], [], [], [], [], [], []

                    for partner in data_c.get('apropos', []):
                        partner_values = {
                            'nom_partenaire': partner.get('nom_partenaire'),
                            'age': partner.get('age'),
                            'pourcentage': partner.get('pourcentage'),
                            'statut_partenaire': partner.get('statut_partenaire'),
                            'nationalite': self.env['res.country'].sudo().browse(int(partner.get('country'))).id if partner.get('country') else None,
                            'lead_id': opportunity.id
                        }
                        partner_record = self.env['wk.partenaire'].sudo().create(
                            partner_values)
                        partner_ids.append(partner_record.id)

                    for manager in data_c.get('gestion', []):
                        gestion_values = {
                            'name': manager.get('name'),
                            'job': manager.get('job'),
                            'niveau_etude': manager.get('niveau_etude'),
                            'age': int(manager.get('age')),
                            'experience': int(manager.get('experience')),
                            'lead_id': opportunity.id
                        }
                        gestion_record = self.env['wk.gestion'].sudo().create(
                            gestion_values)
                        gestion_ids.append(gestion_record.id)

                    for taille in data_c.get('tailles', []):
                        taille_values = {
                            'type_demande': self.env['wk.product'].sudo().search([('id', '=', taille['type_demande'])], limit=1).id,
                            'montant': float(taille.get('montant', 0.0)),
                            'raison': taille.get('raison'),
                            'preg': float(taille.get('preg', 0.0)),
                            'duree': int(taille.get('duree', 0)),
                            'garanties': [(6, 0, [int(garantie_id.get("id")) for garantie_id in taille.get('garanties', [])])],
                            'lead_id': opportunity.id
                        }
                        taille_record = self.env['wk.taille'].sudo().create(taille_values)
                        taille_ids.append(taille_record.id)

                    for situation in data_c.get('situations', []):
                        situation_values = {
                            'banque': self.env['wk.banque'].sudo().browse(int(situation['banque'])).id if situation.get('banque') else None,
                            'type_fin': self.env['wk.fin.banque'].sudo().browse(int(situation['typeFin']['id'])).id if situation.get('typeFin') else None,
                            'montant': float(situation.get('montant')),
                            'encours': float(situation.get('encours')),
                            'garanties': situation.get('garanties',''),
                            'lead_id': opportunity.id
                        }
                        situation_record = self.env['wk.situation'].sudo().create(
                            situation_values)
                        situation_ids.append(situation_record.id)

                    for supplier in data_c.get('fournisseurs', []):
                        supplier_values = {
                            'name': supplier.get('name'),
                            'country': self.env['res.country'].sudo().browse(int(supplier.get('country'))).id if supplier.get('country') else None,
                            'type_payment': [(6, 0, [int(payment_id.get('id')) for payment_id in supplier.get('type_payment', [])])],
                            'lead_id': opportunity.id
                        }
                        supplier_record = self.env['wk.fournisseur'].sudo().create(
                            supplier_values)
                        fournisseur_ids.append(supplier_record.id)

                    for client in data_c.get('clients', []):
                        client_values = {
                            'name': client.get('name'),
                            'country': self.env['res.country'].sudo().browse(int(client.get('country'))).id if client.get('country') else None,
                            'type_payment': [(6, 0, [int(payment_id.get('id')) for payment_id in client.get('type_payment', [])])],
                            'lead_id': opportunity.id
                        }
                        client_record = self.env['wk.client'].sudo().create(client_values)
                        client_ids.append(client_record.id)
                    
                    for company in data_c.get('companies', []):
                        company_values = {
                            'name': company.get('name'),
                            'date_creation': company.get('date_creation'),
                            'chiffre_affaire': company.get('chiffre_affaire'),
                            'n1_num_affaire': company.get('n1_num_affaire'),
                            'n_num_affaire': company.get('n_num_affaire'),
                        }
                        company_record = self.env['wk.companies'].sudo().create(company_values)
                        company_ids.append(company_record.id)

                    opportunity.sudo().write({
                        'apropos': [(6, 0, partner_ids)],
                        'gestion': [(6, 0, gestion_ids)],
                        'tailles': [(6, 0, taille_ids)],
                        'fournisseurs': [(6, 0, fournisseur_ids)],
                        'clients': [(6, 0, client_ids)],
                        'situations': [(6, 0, situation_ids)],
                        'companies': [(6, 0, company_ids)],

                    })

                    _logger.info('Opportunity step 3 created ')


                except Exception as e:
                    _logger.error('Opportunity step 3 not created ')
                    _logger.error(f'step not created because:{e}')
                try:
                    
                    for document in data_c.get('documents', []):
                        document_values = {
                            'list_document': document.get('list_document'),
                            'list_doc':  document.get('list_doc'),
                            'document': base64.b64decode(document.get('document')) if document.get('document') else False,

                            'lead_id': opportunity.id
                        }
                        self.env['wk.document.check'].sudo().create(document_values)
                    _logger.info('Documents created successfully.')
                except Exception as e:
                    _logger.error('Error creating documents: %s', e)
                    
            _logger.info('All records processed successfully.')
            ids_response = session.post(f'{base_url}/opportunity/confirm_get_opportunities', json={'ids': ids_recieved},verify=False,  timeout=10)
            ids_response.raise_for_status()
            _logger.info('IDs sent back successfully: %s', ids_recieved)

            _logger.info('HTTP request processed successfully.')
        except requests.RequestException as e:
            _logger.error('Data fetch failed: %s', e)
