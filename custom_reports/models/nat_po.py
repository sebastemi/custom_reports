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
    delivery_place = fields.Char('Shipping Mark / Lugar de Entrega', readonly=True) #DEPRECATED
    delivery_place_list = fields.Selection(
        [
            ('default','TEMI, C.A. VALENCIA - VENEZUELA RIF J-07508517-5'),
            ('supplier_place','INSTALACIONES DEL PROVEEDOR'),
            ('client_place','INSTALACIONES DEL CLIENTE'),
            ('plant_place','PLANTA TEMI TOCUYITO'),
            ('rotoval','OFICINA ROTOVAL'),
        ],
        string='Shipping Mark / Lugar de Entrega'
    )
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
    insurance = fields.Char(string='Seguro', readonly=True) # DEPRECATED
    insurance_list = fields.Selection(
        [
            ('our','OUR'),
            ('yours','YOUR'),
            ('no_apply','N/A')
        ],
        string='Seguro'
    )
    att = fields.Char(string='ATT')
    type_of_packing = fields.Char(string='Tipo de Empaquetamiento', readonly=True) # DEPRECATED
    type_of_packing_list = fields.Selection(
        [
            ('export','EXPORT PACKING'),
            ('import','IMPORT PACKING'),
            ('no_apply','N/A')
        ], 
        string='Tipo de Empaquetamiento'
    )
    regimen = fields.Char('Regimen', readonly=True) # DEPRECATED
    regimen_list = fields.Selection(
        [
            ('own_funds','FONDOS PROPIOS'),
        ], 
        string='Regimen'
    )
    wo_showed = fields.Selection(
        [
            ('USO INTERNO','USO INTERNO'),
            ('ot','ORDEN DE TRABAJO')
        ], 
        string='OT Mostrada en reporte'
    )
    studio_approver_ids = fields.Many2many(
        comodel_name='res.users',
        compute='_compute_studio_approvers',
        string='Aprobadores'
    )

    @api.depends('state')
    def _compute_studio_approvers(self):
        # 1. Buscamos todas las entradas de aprobación de Studio exitosas para estos registros
        approvals = self.env['studio.approval.entry'].search([
            ('model', '=', 'purchase.order'),
            ('res_id', 'in', self.ids),
            ('approved', '=', True)
        ])
        
        
        # 2. Asignamos los usuarios a la orden correspondiente
        for order in self:
            users = approvals.filtered(lambda a: a.res_id == order.id).mapped('user_id')
            order.studio_approver_ids = [(6, 0, users.ids)]
    
    def button_confirm(self):
        res = super(NationalPurshaseOrder, self).button_confirm()
        
        for order in self:
            if order.partner_id:
                order.message_unsubscribe(partner_ids=order.partner_id.ids)
                
        return res

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
