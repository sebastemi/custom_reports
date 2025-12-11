from odoo import fields, api, models
from num2words import num2words
import math


class InventoryReport(models.Model):
    _inherit = 'stock.picking'

    control_index = fields.Char()
    delivery_order = fields.Char()
    delivery_date = fields.Date()
    company_name = fields.Char()
    company_address = fields.Text()
    tin = fields.Char()
    tin_client = fields.Char()
    work_order = fields.Char()
    purshase_order = fields.Char()
    pay_conditions = fields.Char()
    pay_method = fields.Char()
    transport = fields.Char()
    currency_id = fields.Many2one('res.currency')
    spell_amount = fields.Text(compute='_compute_spell_amount')
    subtotal = fields.Monetary(currency_field='currency_id')
    iva = fields.Monetary(currency_field='currency_id')
    total = fields.Monetary(currency_field='currency_id')

    @api.depends('total', 'currency_id') 
    def _compute_spell_amount(self):
        for record in self:
            if record.total and record.currency_id:
                total_rounded = record.currency_id.round(record.total)
                fractional, integer = math.modf(total_rounded)
                letter_amount = num2words(int(integer), lang='es')
                cents = round(fractional * 100)
                record.spell_amount = f" {letter_amount.capitalize()} y {cents:02d} Centavos"
            else:
                record.spell_amount = ""


    def download(self):
        return self.env.ref('custom_reports.report_stock_picking_custom').report_action(self)