from odoo import fields, models, api
from odoo.exceptions import ValidationError 

class NationalPurshaseOrder(models.Model):
    _inherit = 'purchase.order'

    CURRENCIES = [('VES','VES'),('USD','USD'),('EUR','EUR')]
    TRANSPORTS = [('PROVEEDOR','PROVEEDOR'),('CLIENTE','CLIENTE')]

    supplier = fields.Char('Proveedor')
    supplier_direction = fields.Char('Dirección')
    revision = fields.Integer('REV.')
    rif = fields.Char('RIF')
    city = fields.Char('Ciudad')
    country = fields.Char('País')
    purchase_order_number = fields.Char('Orden de compra')
    requisition = fields.Char('Requisicion')
    order_date = fields.Date('Fecha de orden')
    delivery_date = fields.Date('Fecha de entrega')
    delivery_place = fields.Char('Shipping Mark / Lugar de Entrega')
    worker_order = fields.Char('Orden de trabajo')
    payment_conditions = fields.Char('Condiciones de Pago')
    transport = fields.Selection(TRANSPORTS ,'transporte')
    sub_total = fields.Monetary('Subtotal')
    iva = fields.Monetary('IVA')
    total = fields.Monetary('Total')
    requires_quality_report = fields.Boolean('Requiere reporte de calidad')
    requires_test_protocol = fields.Boolean('Requiere protocolo de prueba')
    requires_warranty_certificate = fields.Boolean('Requiere certificado de garantía')
    requires_test_insitu = fields.Boolean('Requiere prueba en sitio')
    requires_calibration_certificate = fields.Boolean('Requiere Certificado de Calibracion')
    is_applied = fields.Boolean('No Aplica')
    currency = fields.Selection(CURRENCIES,'Moneda')
    currency_rate_usd = fields.Float('Tasa USD')
    currency_rate_eur = fields.Float('Tasa EUR')
    currency_rate_usd_to_eur = fields.Float('Conversion USD a EUR')
    annotations = fields.Text('Note')
    created_by_id = fields.Many2one('res.users','Elaborado Por')
    reviewed_by_id = fields.Many2one('res.users','Revisado Por')
    approved_by_id = fields.Many2one('res.users','Aprobado Por')
    order_terms = fields.Text('Terminos de Orden')
    insurance = fields.Char(string='Seguro')
    att = fields.Char(string='ATT')
    type_of_packing = fields.Char(string='Tipo de Empaquetamiento')
    regimen = fields.Char('Regimen')
    wo_showed = fields.Selection(
        [
            ('intern','USO INTERNO'),
            ('ot','ORDEN DE TRABAJO')
        ], 
        string='OT Mostrada en reporte'
    )

class PuchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    custom_note = fields.Text('Nota')

    def action_open_note_wizard(self):

        return {
            'name': f'Notas de {self.product_id.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'custom_reports.note_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_description': self.custom_note,
                'model_name': self._name,
                'model_id': self.id,
            },
        }
