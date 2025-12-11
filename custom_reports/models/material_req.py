from odoo import models, fields, api

class MaterialRequestnReport(models.Model):
    _inherit = 'purchase.order'
    
    req_date = fields.Date('Fecha de Solicitud')
    req_expected_date = fields.Date('Fecha Requerida')
    req_ot = fields.Char('OT')
    req_client = fields.Char('Cliente')
    req_serial = fields.Char('Lanzamiento Numero')
    req_created_by = fields.Char('Elaborado por')
    req_received_by = fields.Char('Recibido por')
    req_approved_by = fields.Char('Aprobado por')
    req_notes = fields.Text('Observaciones')