from odoo import models, fields, api

class LeadTime(models.Model):
    _name = 'lead.time'
    _description = "Product leadtime based on category"

    name = fields.Char(string='Lead time', required=True)
    days_number = fields.Integer(string='Number of Days', required=True)

class ProductCategory(models.Model):
    _inherit = 'product.category'

    lead_time = fields.Many2one("lead.time", string="Default Lead Time")