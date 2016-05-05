# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010-Today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from openerp.osv import osv
from openerp.osv import fields
from openerp import tools


class send_mail_message(osv.TransientModel):
    _name = 'send.mail.message'
    _description = 'Email composition wizard'

    _columns = {
        'email_to': fields.char('Email To'),
        'attachment_ids': fields.many2many('ir.attachment',
            'send_mail_message_attachments_rel',
            'wizard_id', 'attachment_id', 'Attachments'),
        'subject': fields.char('Subject'),
        'body': fields.html('Body'),
    }

    #------------------------------------------------------
    # Wizard validation and send
    #------------------------------------------------------

    def send_mail(self, cr, uid, ids, context=None):
        attachment_ids = []
#Get Current user record id 
        active_id=context.get('active_id')
        mail_mail = self.pool.get('mail.mail')
        ir_attachment_obj = self.pool.get('ir.attachment')
#        Compose mail
        for wizard in self.browse(cr, uid, ids, context=context):
            if wizard.body and not wizard.body == '<br>':  # when deleting the message, cleditor keeps a <br>
                # add signature
                user_id = self.pool.get("res.users").read(cr, uid, [uid], fields=["signature"], context=context)[0]
                signature = user_id and user_id["signature"] or ''
                if signature:
                    wizard.body = tools.append_content_to_html(wizard.body, signature, plaintext=True, container_tag='div')
#    Get mail attachements
                for data in wizard.attachment_ids:
                    attachment_data = {
                        'name': data.name,
                        'datas_fname': data.datas_fname,
                        'datas': data.datas,
                        'res_model': mail_mail._name,
                    }
                    attachment_ids.append(ir_attachment_obj.create(cr, uid, attachment_data, context=context))
#    Compose mail subject,body and mail to address
                    mail_id = mail_mail.create(cr, uid, {
                                    'email_to':wizard.email_to,
                                    'subject':wizard.subject,
                                    'attachment_ids':[(6, 0, attachment_ids)],
                                    'body_html': '%s' % wizard.body,
                                    }, context=context)
#    Send composed mail with attachments
                    mail_mail.send(cr, uid, [mail_id], context=context)
                    self.pool.get('mail.message').create(cr, uid, {'body':wizard.body,'model':'res.partner','subject':wizard.subject,'res_id':active_id,'message_id':mail_id,'type':'comment','author_id':uid}, context=context)

        return {'type': 'ir.actions.act_window_close'}

