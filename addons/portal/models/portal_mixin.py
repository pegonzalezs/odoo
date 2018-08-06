# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import uuid
import hashlib
import hmac
from werkzeug.urls import url_encode
from odoo import api, exceptions, fields, models, tools, _


class PortalMixin(models.AbstractModel):
    _name = "portal.mixin"

    access_url = fields.Char(
        'Portal Access URL', compute='_compute_access_url',
        help='Customer Portal URL')
    access_token = fields.Char('Security Token', copy=False)

    # to display the warning from specific model
    access_warning = fields.Text("Access warning", compute="_compute_access_warning")

    def _compute_access_warning(self):
        for mixin in self:
            mixin.access_warning = ''

    @api.multi
    def _compute_access_url(self):
        for record in self:
            record.access_url = '#'

    def _portal_ensure_token(self):
        """ Get the current record access token """
        self.access_token = self.access_token if self.access_token else str(uuid.uuid4())
        return self.access_token

    def _get_share_url(self, redirect=False, signup_partner=False, pid=None):
        """
        Build the url of the record  that will be sent by mail and adds additional parameters such as
        access_token to bypass the recipient's rights,
        signup_partner to allows the user to create easily an account,
        hash token to allow the user to be authenticated in the chatter of the record portal view, if applicable
        :param redirect : Send the redirect url instead of the direct portal share url
        :param signup_partner: allows the user to create an account with pre-filled fields.
        :param pid: = partner_id - when given, a hash is generated to allow the user to be authenticated
            in the portal chatter, if any in the target page,
            if the user is redirected to the portal instead of the backend.
        :return: the url of the record with access parameters, if any.
        """
        self.ensure_one()
        params = {
            'model': self._name,
            'res_id': self.id,
        }
        if hasattr(self, 'access_token'):
            params['access_token'] = self._portal_ensure_token()
        if pid:
            params['pid'] = pid
            params['hash'] = self._sign_token(pid)
        if signup_partner and hasattr(self, 'partner_id') and self.partner_id:
            params.update(self.partner_id.signup_get_auth_param()[self.partner_id.id])

        return '%s?%s' % ('/mail/view' if redirect else self.access_url, url_encode(params))

    @api.multi
    def _notify_get_groups(self, message, groups):
        access_token = self._portal_ensure_token()
        customer = self['partner_id']

        if access_token and customer:
            additional_params = {
                'access_token': self.access_token,
            }
            additional_params.update(customer.signup_get_auth_param()[customer.id])
            access_link = self._notify_get_action_link('view', **additional_params)

            new_group = [
                ('portal_customer', lambda partner: partner.id == customer.id, {
                    'has_button_access': False,
                    'button_access': {
                        'url': access_link,
                        'title': ('View %s') % self.env['ir.model']._get(message.model).display_name,
                    },
                })
            ]
        else:
            new_group = []
        return super(PortalMixin, self)._notify_get_groups(message, new_group + groups)

    @api.multi
    def get_access_action(self, access_uid=None):
        """ Instead of the classic form view, redirect to the online document for
        portal users or if force_website=True in the context. """
        self.ensure_one()

        user, record = self.env.user, self
        if access_uid:
            try:
                record.check_access_rights('read')
                record.check_access_rule("read")
            except exceptions.AccessError:
                return super(PortalMixin, self).get_access_action(access_uid)
            user = self.env['res.users'].sudo().browse(access_uid)
            record = self.sudo(user)
        if user.share or self.env.context.get('force_website'):
            try:
                record.check_access_rights('read')
                record.check_access_rule('read')
            except exceptions.AccessError:
                if self.env.context.get('force_website'):
                    return {
                        'type': 'ir.actions.act_url',
                        'url': record.access_url,
                        'target': 'self',
                        'res_id': record.id,
                    }
                else:
                    pass
            else:
                return {
                    'type': 'ir.actions.act_url',
                    'url': record._get_share_url(),
                    'target': 'self',
                    'res_id': record.id,
                }
        return super(PortalMixin, self).get_access_action(access_uid)

    @api.model
    def action_share(self):
        action = self.env.ref('portal.portal_share_action').read()[0]
        action['context'] = {'active_id': self.env.context['active_id'],
                             'active_model': self.env.context['active_model']}
        return action

    @api.multi
    def _sign_token(self, pid):
        """Generate a secure hash for this record with the email of the recipient with whom the record have been shared.

        This is used to determine who is opening the link
        to be able for the recipient to post messages on the document's portal view.

        :param str email:
            Email of the recipient that opened the link.
        """
        self.ensure_one()
        secret = self.env["ir.config_parameter"].sudo().get_param(
            "database.secret")
        token = (self.env.cr.dbname, self.access_token, pid)
        return hmac.new(secret.encode('utf-8'), repr(token).encode('utf-8'), hashlib.sha256).hexdigest()
