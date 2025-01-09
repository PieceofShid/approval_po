from odoo import models, fields, api, _

class ApprovalConfig(models.Model):
    _name = 'ics.approval.po.config'
    _description = 'Configuration approval for purchase order'

    name = fields.Char(string='Reference', required=True, default="Approval Purchase Order")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    rule_id = fields.One2many('ics.approval.po.rule', 'approval_config_id', string='Approval PO Rule')
    active = fields.Boolean(string="Active", default=False)

class ApprovalRule(models.Model):
    _name = 'ics.approval.po.rule'
    _description = 'Rule approval for purchase order based on users and amount'

    approval_config_id = fields.Many2one('ics.approval.po.config', string="Config Reference", required=True, ondelete="cascade", index=True, copy=False)
    name = fields.Char(string='Action Reference', required=True)
    state = fields.Selection(string='State', required=True, selection=[
        ('draft', 'Draft'),
        ('pending_release_1', 'Pending Release 1'),
        ('pending_release_2', 'Pending Release 2'),
        ('pending_release_3', 'Pending Release 3'),
        ('waiting_release_1', 'Waiting Release 1'),
        ('waiting_release_2', 'Waiting Release 2'),
        ('waiting_release_3', 'Waiting Release 3'),
        ('waiting_complete', 'Waiting Complete'),
        ('complete', 'Complete'),])
    action = fields.Selection(string='Action', required=True, selection=[
        ('pending_release_1', 'Pending Release 1'),
        ('pending_release_2', 'Pending Release 2'),
        ('pending_release_3', 'Pending Release 3'),
        ('waiting_release_1', 'Waiting Release 1'),
        ('waiting_release_2', 'Waiting Release 2'),
        ('waiting_release_3', 'Waiting Release 3'),
        ('waiting_complete', 'Waiting Complete'),
        ('complete', 'Complete'),])
    users = fields.Many2many('res.users', string='Users', required=True)
    currency_field = fields.Many2one("res.currency", string="Currency", required=True,
        default=lambda self: self.env.company.currency_id.id)
    minimal_amount = fields.Monetary(string="Minimal Amount", required=True, currency_field="currency_field")
    maximal_amount = fields.Monetary(string="Maximal Amount", required=True, currency_field="currency_field")

    @api.onchange('action')
    def _update_name(self):
        generate_name = dict(self._fields['action']._description_selection(self.env)).get(self.action)

        self.name = generate_name
