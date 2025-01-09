from odoo import models, fields, _

class RejectWizard(models.TransientModel):
    _name = 'ics.approval.po.reject'

    purchase = fields.Many2one('purchase.order', string='Purchase Order', default=lambda self: self._context.get('active_id'))
    reasons = fields.Text(string="Rejected Reasons", required=True)

    def reject_purchase_order(self):
        self.purchase.write({
            'state': 'reject'
        })
        self.purchase.message_post(body=_("Your %s has been rejected by %s with reasons: %s", self.purchase.name, self.env.user.name, self.reasons))

        return self