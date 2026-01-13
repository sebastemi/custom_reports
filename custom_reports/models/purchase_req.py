from odoo import models, fields, api

class PurchaseRequestnReport(models.Model):
    _inherit = 'purchase.order'
    
    preq_date = fields.Date('Fecha de Solicitud')
    preq_expected_date = fields.Date('Fecha Requerida')
    preq_ot = fields.Char('OT')
    preq_client = fields.Char('Cliente')
    preq_serial = fields.Char('Lanzamiento Numero')
    preq_created_by = fields.Char('Elaborado por')
    preq_received_by = fields.Char('Recibido por')
    preq_approved_by = fields.Char('Aprobado por')
    preq_notes = fields.Text('Observaciones')
    preq_type = fields.Selection([('NACIONAL','NACIONAL'), ('IMPORTADO','IMPORTADO')], 'Tipo')
    preq_po = fields.Char('OC')