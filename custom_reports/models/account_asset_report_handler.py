from odoo import models, api

class AccountAssetReportHandler(models.AbstractModel):
    # Heredamos el gestor personalizado exacto del reporte de depreciación
    _inherit = 'account.asset.report.handler'

    @api.model
    def _get_custom_columns_config(self, options):
        # Retrieve the baseline columns
        columns = super()._get_custom_columns_config(options)
        
        # Define and append your custom column definition
        columns.append({
            'name': 'method_number',
            'estimated_width': 15,
            'blank_if_zero': True,
        })
        return columns
    

    @api.model
    def _dynamic_lines_generator(self, options, line_id=None):
        # Get baseline rows from the core method
        lines = super()._dynamic_lines_generator(options, line_id=line_id)
        
        for line in lines:
            # Locate the relevant database record mapped to the row
            res_id = line.get('res_id')
            model = line.get('model')
            
            if model == 'account.asset' and res_id:
                asset = self.env['account.asset'].browse(res_id)
                
                # Fetch your custom value from the record
                custom_value = asset.method_number or 0.0
                
                # Append the cell formatting dictionary into the row's column array
                line['columns'].append({
                    'name': self.format_value(custom_value, options=options),
                    'no_format': custom_value,
                    'class': 'number',
                })
            else:
                # Add an empty cell layout for totals or header rows
                line['columns'].append({'name': ''})
                
        return lines