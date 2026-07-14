import re
from odoo import models

class AccountAssetReportHandler(models.AbstractModel):
    _inherit = 'account.asset.report.handler'

    def _custom_line_postprocessor(self, report, options, lines, warnings=None):
        res = super()._custom_line_postprocessor(report, options, lines, warnings=warnings)

        # Buscamos tu columna 'method_period'
        method_period_index = None
        for i, col in enumerate(options.get('columns', [])):
            if col.get('expression_label') == 'method_period':
                method_period_index = i
                break

        if method_period_index is None:
            return res

        for line in res:
            line_id = str(line.get('id', ''))
            
            # ¡EL TRUCO MÁGICO!
            # Esta expresión regular busca "account.asset" seguido de cualquier 
            # símbolo no numérico, y extrae los números del ID.
            # Funciona con '-account.asset-123', '~account.asset~123', etc.
            match = re.search(r'account\.asset\D+(\d+)', line_id)
            
            if match:
                # Sacamos el ID numérico limpio
                asset_id = int(match.group(1))
                asset = self.env['account.asset'].browse(asset_id)
                
                if asset.exists():
                    # Como configuraste la columna como "Cadena" (String), lo convertimos
                    valor = str(asset.method_period) if asset.method_period else ''
                    
                    # Inyectamos el valor en la celda correspondiente
                    if len(line['columns']) > method_period_index:
                        line['columns'][method_period_index]['name'] = valor
                        line['columns'][method_period_index]['no_format'] = valor

        return res