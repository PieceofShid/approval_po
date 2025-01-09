from odoo import models, fields, api
from datetime import timedelta, datetime

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order.line'

    lead_time = fields.Date(string='Lead Time')

    @api.onchange('product_id')
    def onchange_product(self):
        product = self.env['product.template'].search([('id', '=', self.product_id.id)], limit=1)
        categories = self.env['product.category'].search([('id', '=', product.categ_id.id)], limit=1)

        if(categories.lead_time):
            day = categories.lead_time.days_number
        else:
            day = 0
    
        self.lead_time = (datetime.now() + timedelta(days=day)).date()
        
