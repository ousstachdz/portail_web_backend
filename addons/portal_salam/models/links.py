from odoo import models, fields, api, _
import random

from odoo.exceptions import ValidationError
import string
from datetime import timedelta

from ..__constants__ import BASE_URL, DATABASE, PASSWORD, USERNAME, HOST
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout

import logging

_logger = logging.getLogger(__name__)


class Links(models.Model):
    _name = 'ponctual.links'
    _description = 'Ponctual Links'
    _rec_name = 'display_name'
    
    display_name = fields.Char(string='Display Name', compute='_compute_display_name')
    email = fields.Char(string='البريد الإلكتروني', required=True)
    link = fields.Char(string='الرابط', compute='_compute_link')
    link_uid = fields.Char(string='UID Link', compute='_compute_link_uid', store=True)
    user_id = fields.Many2one('res.users', string='المسؤول عن إنشاء الرابط', default=lambda self: self.env.user, store=True)
    created_at = fields.Datetime(string='تم إنشاؤه في', default=fields.Datetime.now)
    expired_at = fields.Datetime(string='تاريخ انتهاء الصلاحية', compute='_compute_expired_at')
    is_valid = fields.Boolean(string='هل الرابط صالح للاستخدام', compute='_compute_is_valid', default=False)
    is_used = fields.Boolean(string='هل تم استخدامه', default=False)
    is_inactive = fields.Boolean(string='هل تم استخدامه', default=False)

    @api.constrains('email')
    def check_rec(self):
        for rec in self:
            if not rec._check_is_valid_email():
                raise ValidationError("البريد الإلكتروني غير صالح")

            # duplicate_records = self.search([
            #     ('email', '=', rec.email),
            #     ('id', '!=', rec.id),
            # ])

            # if duplicate_records:
            #     raise ValidationError("لا يمكنك إنشاء رابطين بنفس البريد الإلكتروني!")
            
    @api.depends('user_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.user_id.name
    
    @api.depends('user_id')
    def _compute_user_id(self):
        for record in self:
            record.user_id = self.env.user

    @api.depends('link_uid')
    def _compute_link(self):
        for record in self:
            if record.link_uid:
                # host = HOST

                record.link = f'{BASE_URL}/portal-salam/{record.link_uid}'
             
    @api.depends('user_id')
    def _compute_link_uid(self):
        for record in self:
            if not record.link_uid:
                characters = string.ascii_letters + string.digits
                random_string = ''.join(random.choices(characters, k=32))
                record.link_uid = random_string

    @api.depends('created_at', 'is_used')            
    def _compute_is_valid(self):
        for record in self:
            if record.created_at:
                record.is_valid = record.created_at + timedelta(days=1) > fields.Datetime.now() and not record.is_used
            else:
                record.is_valid = False
                
    @api.depends('created_at')
    def _compute_expired_at(self):
        for record in self:
            if record.created_at:
                record.expired_at = record.created_at + timedelta(days=1)
            else:
                record.expired_at = False
    
    def _get_customer_information(self):

        return {
            'customer_name':  self.email,  
            'customer_email': self.email,  
        }
         
    @api.model
    def create(self, vals):
        record = super(Links, self).create(vals)
        record._compute_link_uid()
        record._compute_link()
        record.send_http_request()

        return record


    def send_http_request(self):
        session = requests.Session()
        base_url = BASE_URL

        login_payload = {
            "params": {
                "login": USERNAME,
                "password": PASSWORD,
                "db": DATABASE
            }
        }

        try:
            login_response = session.post(f'{base_url}/web/session/authenticate', json=login_payload, verify=False, timeout=10)
            login_response.raise_for_status()
            login_data = login_response.json()
            _logger.info('Login successful: %s', login_data)
        except RequestException as e:
            _logger.error('Login failed: %s', e)
            return

        read_payload = {
            'email': self.email,
            'link_hash': self.link_uid
        }

        try:
            data_response = session.post(f'{base_url}/link/create', json=read_payload, verify=False, timeout=10)
            data_response.raise_for_status()
            _logger.info('Data fetch successful: %s', data_response.text)
        except (ConnectionError, Timeout) as e:
            _logger.warning('Temporary network issue: %s', e)
        except RequestException as e:
            _logger.error('Data fetch failed: %s', e)
        except Exception as e:
            _logger.exception('Unexpected error while sending request: %s', e)
    def _check_is_valid_email(self):
        import re
        email = self.email
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return True
        else:
            return False

    def action_create_link(self):
        if self._check_is_valid_email():    
            for rec in self:
                rec.write({
                    'email': self.email,
                })
            
                ctx = rec._send_link_email()
                            
                return {
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'mail.compose.message',
                    'target': 'new',
                    'context': ctx,
                }
        else:
            raise ValidationError(_('Invalid email address. Please provide a valid email.'))
            

    def _send_link_email(self):
        self._check_is_valid_email()
        self.ensure_one()
        email_template = self.env['mail.template'].create({
            'name': 'Email Template',
            'model_id': self.env['ir.model']._get('ponctual.links').id,
            'subject': 'إكمال عملية التسجيل - ببنك السلام',
            'email_from': 'no_replay@alsalamalgeria.dz',
            'email_to': self.email,
            'body_html': f'''
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #333; direction: rtl;">
            
            <!-- Main content -->
            <div style="padding: 30px 20px;">
                <h2 style="color: #f2643b;">السادة العملاء الكرام،</h2>
                
                <p>نشكركم لاختياركم <strong style="color: #f2643b;">ببنك السلام</strong> لخدماتكم المصرفية. نقدر ثقتكم في خدماتنا.</p>
                
                <p>لإكمال عملية التسجيل، يرجى الضغط على الرابط أدناه:</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{self.link}" style="background-color: #f2643b; color: white; padding: 12px 25px; 
                       text-decoration: none; border-radius: 4px; font-weight: bold; display: inline-block;">
                        إكمال عملية التسجيل
                    </a>
                </div>
                
                <p>هذا الرابط صالح لفترة محدودة. إذا لم تطلب هذا التسجيل، يرجى تجاهل هذه الرسالة.</p>
                
                <p>للحصول على المساعدة، يرجى الاتصال بخدمة العملاء على <a href="mailto:support@alsalamalgeria.dz" style="color: #f2643b;">support@alsalamalgeria.dz</a>.</p>
                
                <p>مع أطيب التحيات،<br>
                <strong>فريق ببنك السلام</strong></p>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #f5f5f5; padding: 15px 20px; text-align: center; font-size: 12px;">
                <p>© 2023 ببنك السلام. جميع الحقوق محفوظة.</p>
                <p>العنوان: 233, شـارع اْحمـد واكـد دالـي ابراهيـم الجزائـر | الهاتف: </p>
            </div>
        </div>
        ''',
        })
        
        return{
            'default_model': 'ponctual.links',
            'default_res_ids': [self.ids[0]],
            'default_use_template': True,
            'default_template_id': email_template.id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'force_email': True,
        }


    def action_resend_link(self):
        self.ensure_one()
        ctx = self._send_link_email()
                
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'target': 'new',
            'context': ctx,
        }


    def action_deactivate_link(self):
        self.ensure_one()
        self.write({'is_inactive': True})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': 'Link has been deactivated',
                'type': 'success',
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
