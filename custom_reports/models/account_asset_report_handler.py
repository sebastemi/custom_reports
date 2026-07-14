import re
from odoo import models

class AccountAssetReportHandler(models.AbstractModel):
    _inherit = 'account.asset.report.handler'

    def _custom_line_postprocessor(self, report, options, lines, warnings=None):
        res = super()._custom_line_postprocessor(report, options, lines, warnings=warnings)

        # Buscamos los índices de las columnas
        total_months_idx = None
        
        for i, col in enumerate(options.get('columns', [])):
            if col.get('expression_label') == 'total_months_calc': # La nueva etiqueta
                total_months_idx = i

        # Si no existe ninguna de las dos columnas, no perdemos tiempo y salimos
        if total_months_idx is None:
            return res

        # 2. Recorremos las líneas para inyectar los datos
        for line in res:
            line_id = str(line.get('id', ''))
            
            # Buscamos que sea un activo válido
            match = re.search(r'account\.asset\D+(\d+)', line_id)
            if match:
                asset_id = int(match.group(1))
                asset = self.env['account.asset'].browse(asset_id)
                
                if asset.exists():
                    
                    # --- INYECCIÓN: El Cálculo de Meses Totales ---
                    if total_months_idx is not None and len(line['columns']) > total_months_idx:
                        # Aseguramos que sean números enteros antes de multiplicar (por si acaso vienen como string/nulos)
                        m_number = int(asset.method_number) if asset.method_number else 0
                        m_period = int(asset.method_period) if asset.method_period else 0
                        
                        total_meses = m_number * m_period
                        
                        # Lo convertimos a string para que la interfaz lo renderice sin problemas
                        line['columns'][total_months_idx]['name'] = str(total_meses)
                        line['columns'][total_months_idx]['no_format'] = str(total_meses)

        return res