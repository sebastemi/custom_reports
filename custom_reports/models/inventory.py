from odoo import fields, api, models
from num2words import num2words
import math
import re

class InventoryReport(models.Model):
    _inherit = 'stock.picking'

    control_index = fields.Char()
    delivery_order = fields.Char(string="Nota de entrega")
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
    invoice = fields.Char(string="Factura")
    received_by = fields.Many2one('res.users',string="Recibido por")
    project_id = fields.Many2one('project.project',string="Orden de Trabajo")

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
    
class InventoryLineReport(models.Model):
    _inherit = 'stock.move'

    custom_note = fields.Text('Nota')
    position_purchase_order = fields.Integer(
        string='Fila en Orden de Compra',
        compute='_compute_position_purchase_order',
        help='Indica el número de fila que ocupa este producto en la Orden de Compra original.'
    )

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
    
    def extract_data(self, text: str, return_ot: bool) -> str:
        """
        Extrae la OT o el nombre del cliente de una cadena de texto.
        """
        # Regex: Captura "OT-algo", luego ignora espacios y el guion, y captura el resto.
        patron = r'^(OT-[\w]+)\s*-\s*(.*)$'
        match = re.match(patron, text, re.IGNORECASE)
        
        if not match:
            return "Formato inválido"
            
        if return_ot:
            return match.group(1) # Devuelve la OT
        else:
            return match.group(2) # Devuelve el nombre del cliente


    @api.depends('purchase_line_id', 'purchase_line_id.order_id.order_line')
    def _compute_position_purchase_order(self):
        for move in self:
            # 1. Verificamos si este movimiento realmente viene de una compra
            if move.purchase_line_id and move.purchase_line_id.order_id:
                
                # 2. Traemos todas las líneas de esa Orden de Compra.
                # Las ordenamos por 'sequence' (como las acomodó el usuario) y luego por 'id'
                po_lines = move.purchase_line_id.order_id.order_line.sorted(
                    key=lambda l: (l.sequence, l.id)
                )
                
                # 3. Buscamos el índice de nuestra línea dentro de esa lista
                try:
                    # list(po_lines) convierte el recordset en una lista de Python
                    # .index() nos da la posición (empezando en 0, por eso sumamos 1)
                    posicion = list(po_lines).index(move.purchase_line_id) + 1
                    move.posicion_orden_compra = posicion
                except ValueError:
                    # Por si acaso la línea fue eliminada de la orden de compra
                    move.posicion_orden_compra = 0
            else:
                # Si el movimiento es manual o viene de una venta/fabricación, es 0
                move.posicion_orden_compra = 0

class StockMoveLineReport(models.Model):
    _inherit = 'stock.move.line'

    position_purchase_order = fields.Integer(
        related='move_id.position_purchase_order',
        string='Fila en PO',
        readonly=True
    )