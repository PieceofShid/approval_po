from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class ApprovalWizard(models.TransientModel):
    _name = 'ics.approval.po.wizard'
    _description = 'Wizard approval for purchase order'
        
    purchase = fields.Many2one('purchase.order', string='Purchase Order', default=lambda self: self._context.get('active_id'))
    domain_filter = fields.Char(string='Filter Action', compute='get_user_action')
    actions = fields.Many2one('ics.approval.po.rule', string='Action', required=True)

    @api.depends('purchase')
    def get_user_action(self):
        rules = self.env['ics.approval.po.rule'].search([
            ('users', 'in', self.env.uid),
            ('state', '=', self.purchase.state),
            ('minimal_amount', '<', self.purchase.amount_total),
            ('maximal_amount', '>', self.purchase.amount_total)
        ])
        ids = []

        for rule in rules:
            ids.append(rule.id)

        self.domain_filter = [('id', 'in', ids)]

    def _write_approval_log(self):
        history = self.env['ics.approval.po.log']

        if self.purchase.state not in ('sent', 'draf'):
            history.create({
                'purchase_id': self.purchase.id,
                'approver_id': self.env.uid,
                'from_action': dict(self.purchase._fields['state'].selection).get(self.purchase.state),
                'to_action'  : self.actions.name,
            })

    def approve_purchase_order(self):
        action = self.actions.action
        rules  = self.env['ics.approval.po.rule'].search([
            ('state', '=', self.actions.action),
            ('minimal_amount', '<', self.purchase.amount_total),
            ('maximal_amount', '>', self.purchase.amount_total)
        ])

        emails = []
        for user in rules.users:
            emails.append(user.login)

        recipient = ','.join(emails)

        ctx = {
            'status': self.actions.name
        }

        template = self.env.ref('ics_purchase_order.approval_mail_template')
        template.write({'email_to': recipient})
        template.with_context(ctx).send_mail(self.purchase.id, force_send=True)

        self._write_approval_log()

        if action == 'complete':
            return self.purchase.button_approve()
        else:
            return self.purchase.write({
                'state': self.actions.action
            })