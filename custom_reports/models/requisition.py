from odoo import models, fields, api
import re

class RequisitionReport(models.Model):
    _inherit='requisition'


    state_id_name = fields.Char(related='state_id.name')
    reviewed_by_id = fields.Many2one('res.users','Revisado Por')
    approved_by_id = fields.Many2one('res.users','Aprobado Por')
    received_by_id = fields.Many2one('res.users','Recibido Por')


    def _get_xml_report_id(self):

        dict_req_type = {
            'materiales': 'report_material_request_order_custom',
            'compras': 'report_purchase_request_order_custom'
        }

        return dict_req_type[self.type_requisition]


    def action_print_report(self):
        return self.env.ref(f'custom_reports.{self._get_xml_report_id()}').report_action(self)
    
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
    

class RequisitionLineReport(models.Model):
    _inherit='requisition.product.line'

    custom_note = fields.Text('Nota')
    tag_ids = fields.Many2many('requisition.tags', string='Certificaciones')

    def action_open_note_wizard(self):

        return {
            'name': f'Notas de {self.name.name}',
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

class RequisitionTags(models.Model):
    _name = 'requisition.tags'
    _description = 'Etiquetas de Requisición'

    name = fields.Char('Nombre', required=True)
    color = fields.Integer('Color')
