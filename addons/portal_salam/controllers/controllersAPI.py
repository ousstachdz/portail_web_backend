from odoo import http
from odoo.http import request
import json
import base64
List_items = [('1', 'هل العميل شخص مقرب سياسيا؟'),
              ('2', 'هل أحد الشركاء/المساهمين/مسير مقرب سياسيا؟'),
              ('3', 'هل العميل أو أحد الشركاء/المساهمين/مسير مقرب من البنك؟'),
              ('4', 'هل للعميل شركات زميلة / مجموعة؟'),
              ('5', 'المتعامل / أحد الشركاء مدرج ضمن القوائم السوداء'),
              ('6', 'المتعامل / أحد الشركاء مدرج ضمن قائمة الزبائن المتعثرين بمركزية المخاطر لبنك الجزائر')]
LIST = [('1', 'طلب التسهيلات ممضي من طرف المفوض القانوني عن الشركة'),
        ('2', 'الميزانيات لثلاث سنوات السابقة مصادق عليها من طرف المدقق المحاس'),
        ('3',
         ' الميزانية الافتتاحية و الميزانية المتوقعة للسنة المراد تمويلها موقعة من طرف الشركة (حديثة النشأة)'),
        ('4', 'مخطط تمويل الاستغلال مقسم الى أرباع السنة للسنة المراد تمويلها'),
        ('5',
         ' المستندات و الوثائق المتعلقة بنشاط الشركة ( عقود، صفقات ،  طلبيات ، ... )'),
        ('6', 'محاضر الجمعيات العادية و الغير العادية للأشخاص المعنويين'),
        ('7', 'نسخة مصادق عليها من السجل التجاري'),
        ('8', 'نسخة مصادق عليها من القانون الأساسي للشركة'),
        ('9', 'مداولة الشركاء أو مجلس الإدارة لتفويض المسير لطلب القروض البنكية'),
        ('10', 'نسخة مصادق عليها من النشرة الرسمية للإعلانات القانونية'),
        ('11', 'نسخة طبق الأصل لعقد ملكية أو استئجار المحلات ذات الاستعمال المهني'),
        ('12',
         ' نسخة طبق الأصل للشهادات الضريبية و شبه الضريبية حديثة (أقل من ثلاثة أشهر)'),
        ('13', 'استمارة كشف مركزية المخاطر ممضية من طرف ممثل الشركة (نموذج مرفق)'),
        ('14', 'آخر تقرير مدقق الحسابات'),
        ('15', 'Actif, Passif, TCR (N, N-1)'),
        ('16', 'Actif, Passif, TCR (N-2, N-3)')
        ]

list_situation = [
    ('1', 'حقوق الملكية'),
    ('2', 'مجموع الميزانية'),
    ('3', 'رقم الأعمال'),
    ('4', 'صافي الارباح')
]


class OpportunityControllerAPI(http.Controller):

    @http.route(['/portal-salam/<int:user_id>/<string:link_uid>'], type='http', auth='public', website=True, csrf=True)
    def opportunity_api_form(self, user_id, link_uid, **kwargs):

        link = request.env['ponctual.links'].sudo().search(
            [('user_id', '=', user_id), ('link_uid', '=', link_uid)], limit=1)


        if link:
            if link.is_valid:
 
                return request.render('portal_salam.opportunity_api_form', {})
        
        return request.render('portal_salam.opportunity_api_form_error_page', {})

    @http.route(['/opportunity/form_data'], type='http', auth='public',  csrf=True, methods=['GET'], cors='*')
    def opportunity_form(self, **kwargs):
        opportunity_id = kwargs.get('opportunity_id', 0)
        activities = request.env['wk.activite'].search([])
        activities = [{"id": activity.id, "name": activity.name}
                      for activity in activities]
        classifications = request.env['wk.classification'].search([])
        classifications = [{"id": classification.id, "name": classification.name}
                           for classification in classifications]

        demandes = request.env['wk.type.demande'].search([])
        demandes = [{"id": demande.id, "name": demande.name}
                    for demande in demandes]

        forme_jurs = request.env['wk.forme.jur'].search([])
        forme_jurs = [{"id": forme_jur.id, "name": forme_jur.name}
                      for forme_jur in forme_jurs]

        apropos_ids = request.env['wk.partenaire'].search(
            [('lead_id', '=', int(opportunity_id))])
        apropos_ids = [{"id": apropos_id.id, "name": apropos_id.name}
                       for apropos_id in apropos_ids]

        gestion_ids = request.env['wk.gestion'].search(
            [('lead_id', '=', int(opportunity_id))])
        gestion_ids = [{"id": gestion_id.id, "name": gestion_id.name}
                       for gestion_id in gestion_ids]

        taille_ids = request.env['wk.taille'].search(
            [('lead_id', '=', int(opportunity_id))])
        taille_ids = [{"id": taille_id.id, "name": taille_id.name}
                      for taille_id in taille_ids]

        situation_ids = request.env['wk.situation'].search(
            [('lead_id', '=', int(opportunity_id))])
        situation_ids = [{"id": situation_id.id, "name": situation_id.name}
                         for situation_id in situation_ids]

        fournisseur_ids = request.env['wk.fournisseur'].search(
            [('lead_id', '=', int(opportunity_id))])
        fournisseur_ids = [{"id": fournisseur_id.id, "name": fournisseur_id.name}
                           for fournisseur_id in fournisseur_ids]

        client_ids = request.env['wk.client'].search(
            [('lead_id', '=', int(opportunity_id))])
        client_ids = [{"id": client_id.id, "name": client_id.name}
                      for client_id in client_ids]

        company_ids = request.env['wk.companies'].search(
            [('lead_id', '=', int(opportunity_id))])
        company_ids = [{"id": company_id.id, "name": company_id.name}
                       for company_id in company_ids]

        nationalites = request.env['res.country'].search(
            [('to_show', '=', False)])
        nationalites = [{"id": nationality.id, "name": nationality.name}
                        for nationality in nationalites]

        garanties = request.env['wk.garanties'].search([])
        garanties = [{"id": garantie.id, "name": garantie.name}
                     for garantie in garanties]

        type_demande_ids = request.env['wk.product'].search(
            [('for_branch', '=', True)])
        type_demande_ids = [{"id": type_demande_id.id, "name": type_demande_id.name}
                            for type_demande_id in type_demande_ids]
        banque_ids = request.env['wk.banque'].search([])
        banque_ids = [{"id": banque_id.id, "name": banque_id.name}
                      for banque_id in banque_ids]
        type_fin_ids = request.env['wk.fin.banque'].search([])
        type_fin_ids = [{"id": type_fin_id.id, "name": type_fin_id.name}
                        for type_fin_id in type_fin_ids]

        type_payment_ids = request.env['wk.type.payment'].search([])
        type_payment_ids = [{"id": type_payment_id.id, "name": type_payment_id.name}
                            for type_payment_id in type_payment_ids]

        if opportunity_id != 0:
            opportunity = request.env['crm.lead'].sudo().browse(int(opportunity_id))
        else:
            opportunity = False
        situation_fin = request.env['wk.situation.fin'].search(
            [('lead_id', '=', int(opportunity_id))])

        values = {
            'step': opportunity.stage if opportunity else 'step1',
            'opportunity_id': opportunity_id if opportunity_id else 0,
            'activities': activities,
            'nationalites': nationalites,
            'classifications': classifications,
            'demandes': demandes,
            'forme_jurs': forme_jurs,
            'banque_ids': banque_ids,
            'type_fin_ids': type_fin_ids,
            'apropos_ids': apropos_ids,
            'gestion_ids': gestion_ids,
            'taille_ids': taille_ids,
            'kyc_ids': List_items,
            'situation_ids': situation_ids,
            'fournisseur_ids': fournisseur_ids,
            'client_ids': client_ids,
            'company_ids': company_ids,
            'garanties_ids': garanties,
            'answers': [('oui', 'نعم'),
                        ('non', 'لا')],
            'type_demande_ids': type_demande_ids,
            'type_payment_ids': type_payment_ids,
        }

        for index, fin in enumerate(situation_fin):
            values[f'fin{index+1}_1'] = fin.year1
            values[f'fin{index+1}_2'] = fin.year2
            values[f'fin{index+1}_3'] = fin.year3
        for index, fin in enumerate(situation_fin):
            values[f'fin{index+1}_1'] = fin.year1
            values[f'fin{index+1}_2'] = fin.year2
            values[f'fin{index+1}_3'] = fin.year3

        return request.make_response(
            json.dumps(values, default=str),
            headers={'Content-Type': 'application/json'}
        )

    @http.route(['/opportunity/form_data/save'], type='http', auth='public', methods=['POST'], website=True, csrf=False, cors='*')
    def opportunity_submit(self, **post):
        try:
            data = json.loads(request.httprequest.data)
            def handle_empty_date(field):
                return field if field else None
            user_id = data.get('user_id')
            link_hash = data.get('link_hash')
            
            link = request.env['ponctual.links'].sudo().search(
                [('user_id', '=', user_id), ('link_uid', '=', link_hash)], limit=1)

            if not link.is_valid:
                print('error: Invalid link')
                return request.render('portal_salam.opportunity_api_form_error_page', {})

            lead_values = {
                'user_id': data.get('user_id'),
                'name': data.get('name'),
                'phone': data.get('phone'),
                'email_from': data.get('email_from'),
                'adress_siege': data.get('adress_siege'),
                'nif': data.get('nif'),
                'rc': data.get('rc'),
                'num_compte': data.get('num_compte'),
                'date_ouverture_compte': handle_empty_date(data.get('date_ouverture_compte')),
                'date_debut': handle_empty_date(data.get('date_debut')),
                'nom_arabe': data.get('nom_arabe'),
                'date_debut_activite': handle_empty_date(data.get('date_debut_activite')),
                'activity_code': data.get('activity_code'),
                'activity_description': data.get('activity_description'),
                'activite_sec': data.get('activite_sec'),
                'classification': int(data.get('classification')) if data.get('classification') else None,
                'forme_jur': int(data.get('forme_jur')) if data.get('forme_jur') else None,
                'chiffre_affaire': float(data.get('chiffre_affaire', 0.0)),
                'chiffre_affaire_creation': float(data.get('chiffre_affaire_creation', 0.0)),
                'demande': int(data.get('demande')) if data.get('demande') else None,
                'explanation': data.get('explanation'),
                'description_company': data.get('description_company'),
            }

            opportunity = request.env['crm.lead'].sudo().create(lead_values)
            documents = []
            
            document_dict = {item[0]: item[1]
                             # Ensure LIST is defined earlier
                             for item in LIST}

            documents_values = {
                'document_1': data.get('document_1'),
                'document_2': data.get('document_2'),
                'document_3': data.get('document_3'),
                'document_4': data.get('document_4'),
                'document_5': data.get('document_5'),
                'document_6': data.get('document_6'),
                'document_7': data.get('document_7'),
                'document_8': data.get('document_8'),
                'document_9': data.get('document_9'),
                'document_10': data.get('document_10'),
                'document_11': data.get('document_11'),
                'document_12': data.get('document_12'),
                'document_13': data.get('document_13'),
                'document_14': data.get('document_14'),
                'document_15': data.get('document_15'),
                'document_16': data.get('document_16'),
            }


            for key, base64_file in documents_values.items():
                if key.startswith('document_') and base64_file:
                    try:
                        document_id = int(key.split('_')[1])
                        # Ensure the base64_file is a valid string
                        if isinstance(base64_file, str) and base64_file.strip():
                            base64_string = base64_file
                            if base64_string.startswith("dataapplication/pdfbase64"):
                                base64_string = base64_string.replace(
                                    "dataapplication/pdfbase64", "data:application/pdf;base64,")
                            base64_string = base64_string.split(",")[1]
                            base64_string = base64_string + \
                                '=' * (-len(base64_string) % 4)
                            documents.append({
                                'list_document': str(document_id),
                                'list_doc': document_dict.get(str(document_id), ''),
                                'document': base64_string,
                                'lead_id': opportunity.id
                            })
                        else:
                            print(f'Invalid base64 string provided for document {document_id}')
                    except (ValueError, AttributeError) as e:
                        print(f'Error processing document {key}: {e}')
                        continue

            # If documents exist, create or update them
            if documents:
                if not opportunity.documents:
                    request.env['wk.document.check'].sudo().create(documents)
                else:
                    for doc in documents:
                        exist_doc = opportunity.documents.filtered(
                            lambda l: l.list_document == doc['list_document'])
                        if exist_doc:
                            exist_doc.write(doc)

            partner_ids, gestion_ids, taille_ids, fournisseur_ids, client_ids, situation_ids = [
            ], [], [], [], [], []

            for partner in data.get('partners', []):
                partner_values = {
                    'nom_partenaire': partner.get('nom_partenaire'),
                    'age': partner.get('age'),
                    'pourcentage': partner.get('pourcentage'),
                    'statut_partenaire': partner.get('statut_partenaire'),
                    'nationalite': request.env['res.country'].sudo().browse(int(partner.get('country'))).id if partner.get('country') else None,
                    'lead_id': opportunity.id
                }
                partner_record = request.env['wk.partenaire'].sudo().create(
                    partner_values)
                partner_ids.append(partner_record.id)

            for manager in data.get('managers', []):
                gestion_values = {
                    'name': manager.get('name'),
                    'job': manager.get('job'),
                    'niveau_etude': manager.get('niveau_etude'),
                    'age': int(manager.get('age')),
                    'experience': int(manager.get('experience')),
                    'lead_id': opportunity.id
                }
                gestion_record = request.env['wk.gestion'].sudo().create(
                    gestion_values)
                gestion_ids.append(gestion_record.id)

            for taille in data.get('tailles', []):
                taille_values = {
                    'type_demande': request.env['wk.product'].sudo().search([('name', '=', taille['type_demande']['name'])], limit=1).id,
                    'montant': float(taille.get('montant', 0.0)),
                    'raison': taille.get('raison'),
                    'preg': float(taille.get('preg', 0.0)),
                    'duree': int(taille.get('duree', 0)),
                    'garanties': [(6, 0, [int(garantie_id) for garantie_id in taille.get('garanties', [])])],
                    'lead_id': opportunity.id
                }
                taille_record = request.env['wk.taille'].sudo().create(taille_values)
                taille_ids.append(taille_record.id)

            for situation in data.get('situationTailles', []):
                situation_values = {
                    'banque': request.env['wk.banque'].sudo().browse(int(situation['banque']['id'])).id if situation.get('banque') else None,
                    'type_fin': request.env['wk.fin.banque'].sudo().browse(int(situation['typeFin']['id'])).id if situation.get('typeFin') else None,
                    'montant': float(situation.get('situationMontant')),
                    'encours': float(situation.get('situationEncours')),
                    'garanties': ", ".join([g['name'] for g in situation.get('situationGaranties', [])]),
                    'lead_id': opportunity.id
                }
                situation_record = request.env['wk.situation'].sudo().create(
                    situation_values)
                situation_ids.append(situation_record.id)

            for supplier in data.get('suppliers', []):
                supplier_values = {
                    'name': supplier.get('name'),
                    'country': request.env['res.country'].sudo().browse(int(supplier.get('country'))).id if supplier.get('country') else None,
                    'type_payment': [(6, 0, [int(payment_id) for payment_id in supplier.get('selectedPayments', [])])],
                    'lead_id': opportunity.id
                }
                supplier_record = request.env['wk.fournisseur'].sudo().create(
                    supplier_values)
                fournisseur_ids.append(supplier_record.id)

            for client in data.get('clients', []):
                client_values = {
                    'name': client.get('name'),
                    'country': request.env['res.country'].sudo().browse(int(client.get('country'))).id if client.get('country') else None,
                    'type_payment': [(6, 0, [int(payment_id) for payment_id in client.get('selectedPayments', [])])],
                    'lead_id': opportunity.id
                }
                client_record = request.env['wk.client'].sudo().create(client_values)
                client_ids.append(client_record.id)
            answers = {}
            details = {}
            infos = {}
            list_items_dict = {item[0]: item[1] for item in List_items}
            for key, value in data.get('kyc', []):
                if key.startswith('answer_'):
                    try:
                        record_id = int(key.split('_')[1])
                        answers[record_id] = value
                    except ValueError:
                        continue
                elif key.startswith('detail_'):
                    try:
                        record_id = int(key.split('_')[1])
                        details[record_id] = value
                    except ValueError:
                        continue
                elif key.startswith('info_'):
                    try:
                        # Extraire l'ID de la clé
                        record_id = int(key.split('_')[1])
                        infos[record_id] = value
                    except ValueError:
                        continue

            records_to_create = []

            for record_id in answers.keys():
                record = {
                    'answer': answers[record_id],
                    'detail': details.get(record_id, ''),
                    'info': list_items_dict.get(str(record_id), ''),
                    'lead_id': opportunity.id
                }
                records_to_create.append(record)
            if records_to_create:
                request.env['wk.kyc.details'].sudo().create(records_to_create)

            opportunity.sudo().write({
                'apropos': [(6, 0, partner_ids)],
                'gestion': [(6, 0, gestion_ids)],
                'tailles': [(6, 0, taille_ids)],
                'fournisseurs': [(6, 0, fournisseur_ids)],
                'clients': [(6, 0, client_ids)],
                'situations': [(6, 0, situation_ids)],
            })


            name = data.get('name')
            login = data.get('email_from')
            email = data.get('email_from')



            user = request.env['res.users'].sudo().search([('login', '=', login)], limit=1)

            if user:
                print('User with this login already exists')
            else:
                group_portal = request.env.ref(
                    'base.group_portal'
                )
                try:
                    user = request.env['res.users'].sudo().create({
                        'name': name,
                        'login': login,
                        'email': email,
                        'nom_arabe': data.get('nom_arabe') or '',
                        'mobile': data.get('mobile') or '',
                        'website': data.get('website') or '',
                        'groups_id': [(6, 0, [group_portal.id,])],
                    })
                except Exception as e:
                    return {'error': str(e)}
                
            opportunity.sudo().write({'partner_id': user.id})
         
            opportunity.sudo().convert_opportunity(partner=user)
            link.sudo().write({'is_used': True})
            
            return request.make_response(
                json.dumps({'message': 'Data saved successfully',
                           'lead_id':''}),
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            print("Error saving opportunity data: %s" % str(e))
            return request.make_response(
                json.dumps(
                    {'error': 'Failed to save data', 'details': str(e)}),
                headers={'Content-Type': 'application/json'},
                status=500
            )


class WebsiteRedirect(http.Controller):

    @http.route('/', type='http', auth='public', website=True)
    def homepage_redirect(self):
        return request.redirect('/web/login')

