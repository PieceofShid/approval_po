from odoo import models, fields, _
from odoo.tools import format_list
from odoo.exceptions import UserError

class ApprovalPurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    state = fields.Selection(selection_add=[('pending_release_1', 'Pending Release 1'),
        ('pending_release_2', 'Pending Release 2'),
        ('pending_release_3', 'Pending Release 3'),
        ('waiting_release_1', 'Waiting Release 1'),
        ('waiting_release_2', 'Waiting Release 2'),
        ('waiting_release_3', 'Waiting Release 3'),
        ('waiting_complete', 'Waiting Complete'),
        ('purchase',)])
    
    def _get_approval_config_status(self):
        for purchase in self:
            approval = self.env['ics.approval.po.config'].search([], limit=1)
            purchase.is_approval_active = approval.active
    
    is_approval_active = fields.Boolean(string="Is Approval Active", compute=_get_approval_config_status)

    def button_confirm(self):
        approval = self.env['ics.approval.po.config'].search([], limit=1)
        
        if approval.active == False:
            for order in self:
                if order.state not in ['draft', 'sent']:
                    continue
                order.order_line._validate_analytic_distribution()
                order._add_supplier_to_product()
                # Deal with double validation process
                if order._approval_allowed():
                    order.button_approve()
                else:
                    order.write({'state': 'to approve'})
                if order.partner_id not in order.message_partner_ids:
                    order.message_subscribe([order.partner_id.id])

        return True

    def button_cancel(self):
        approval = self.env['ics.approval.po.config'].search([], limit=1)
        
        if approval.active == True:
            logs = self.approval_log.search([
            ('purchase_id', '=', self.id)])

            logs.write({
                'log_active': False
            })
        
        purchase_orders_with_invoices = self.filtered(lambda po: any(i.state not in ('cancel', 'draft') for i in po.invoice_ids))
        if purchase_orders_with_invoices:
            raise UserError(_("Unable to cancel purchase order(s): %s. You must first cancel their related vendor bills.", format_list(self.env, purchase_orders_with_invoices.mapped('display_name'))))
        self.write({'state': 'cancel', 'mail_reminder_confirmed': False})
    
    def send_approval_mail(self):
        rules  = self.env['ics.approval.po.rule'].search([
            ('state', '=', self.state),
            ('minimal_amount', '<', self.amount_total),
            ('maximal_amount', '>', self.amount_total)
        ])

        if rules:
            emails = []
            for user in rules.users:
                emails.append(user.login)

            recipient = ','.join(emails)

            template = self.env.ref('ics_purchase_order.approval_mail_template')
            template.write({'email_to': recipient})
            template.send_mail(self.id, force_send=True)
        else:
            return True

    def _get_approval_log(self):
        logs = self.approval_log.search([
            ('from_action', '!=', 'RFQ'),
            ('to_action', '!=', 'Complete'),
            ('log_active', '=', True),
            ('purchase_id', '=', self.id)],
            order='datetime DESC', limit=1)
        approver = []

        for log in logs:
            approver.append({
                'name': log.approver_id.name,
                'signature': log.approver_id.signature_image
            })

        return approver
    
    def _get_approval_complete(self):
        logs = self.approval_log.search([
            ('to_action', '=', 'Complete'),
            ('log_active', '=', True),
            ('purchase_id', '=', self.id)], order='datetime DESC', limit=1)
        
        return {
            'name': logs.approver_id.name,
            'signature': logs.approver_id.signature_image,
            'date': logs.datetime
        }