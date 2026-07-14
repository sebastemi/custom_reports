import re
from odoo import models

class AccountAssetReportHandler(models.AbstractModel):
    _inherit = 'account.asset.report.handler'

    def _custom_line_postprocessor(self, report, options, lines, warnings=None):
        res = super()._custom_line_postprocessor(report, options, lines, warnings=warnings)

        # Buscamos los índices de las columnas
        total_months_idx = None
        depreciated_months_idx = None
        for i, col in enumerate(options.get('columns', [])):
            if col.get('expression_label') == 'total_months_calc': # La nueva etiqueta
                total_months_idx = i
            elif col.get('expression_label') == 'depreciated_months_calc': # La nueva etiqueta
                depreciated_months_idx = i

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
                        
                        total_months = m_number * m_period
                        
                        # Lo convertimos a string para que la interfaz lo renderice sin problemas
                        line['columns'][total_months_idx]['name'] = str(total_months)
                        line['columns'][total_months_idx]['no_format'] = str(total_months)
                        
                    if depreciated_months_idx is not None and len(line['columns']) > depreciated_months_idx:
                        # 1. Filtramos y contamos cuántos asientos de depreciación están publicados
                        posted_account_move_ids = len(asset.depreciation_move_ids.filtered(lambda m: m.state == 'posted'))
                        
                        # 2. Multiplicamos por el method_period (1 si es mensual, 12 si es anual)
                        m_period = int(asset.method_period) if asset.method_period else 0
                        depreciated_months = posted_account_move_ids * m_period
                        
                        # 3. Inyectamos a la celda
                        line['columns'][depreciated_months_idx]['name'] = str(depreciated_months)
                        line['columns'][depreciated_months_idx]['no_format'] = str(depreciated_months)

        return res