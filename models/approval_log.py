from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    approval_log = fields.One2many('ics.approval.po.log', 'purchase_id', string="Approval Log")
    
class ApprovalLog(models.Model):
    _name = 'ics.approval.po.log'

    purchase_id = fields.Many2one('purchase.order', string="Purchase Order", readonly=True, required=True)
    approver_id = fields.Many2one('res.users', string="Approver")
    from_action = fields.Char(string="From")
    to_action   = fields.Char(string="To")
    datetime    = fields.Datetime(string="Date & Time", default=lambda self: fields.Datetime.now())
    log_active  = fields.Boolean(string="Active", default=True)