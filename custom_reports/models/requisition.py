from odoo import models, fields, api

class RequisitionReport(models.Model):
    _inherit='requisition'


    state_id_name = fields.Char(related='state_id.name')

    def _get_xml_report_id(self):

        dict_req_type = {
            'materiales': 'report_material_request_order_custom',
            'compras': 'report_purchase_request_order_custom'
        }

        return dict_req_type[self.type_requisition]


    def action_print_report(self):
        return self.env.ref(f'custom_reports.{self._get_xml_report_id()}').report_action(self)
    
