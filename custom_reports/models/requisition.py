from odoo import models, fields, api

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
    
class RequisitionLineReport(models.Model):
    _inherit='requisition.product.line'

    custom_note = fields.Text('Nota')

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
