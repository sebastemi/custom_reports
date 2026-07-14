from odoo import models

class AccountAssetReportHandler(models.AbstractModel):
    _inherit = 'account.asset.report.handler'

    def _custom_line_postprocessor(self, report, options, lines, warnings=None):
        """
        Interceptamos las líneas del reporte de depreciación justo antes de imprimirlas.
        """
        # 1. Dejamos que Odoo haga su trabajo normal primero
        res = super()._custom_line_postprocessor(report, options, lines, warnings=warnings)

        # 2. Buscamos el índice (posición) de tu columna 'method_period' en la interfaz
        # options['columns'] tiene la lista de columnas configuradas en la pantalla
        method_period_index = None
        for i, col in enumerate(options.get('columns', [])):
            if col.get('expression_label') == 'method_number':
                method_period_index = i
                break

        # Si no encontró la columna en la pantalla, no hacemos nada
        if method_period_index is None:
            return res

        # 3. Recorremos cada fila (línea) del reporte
        for line in res:
            # Los IDs de las líneas de activos en Odoo 17 suelen tener el formato 'account.asset~ID'
            line_id = str(line.get('id', ''))
            
            if line_id.startswith('account.asset~'):
                try:
                    # Extraemos el ID numérico del activo
                    asset_id = int(line_id.split('~')[1])
                    
                    # Buscamos el activo en la base de datos
                    asset = self.env['account.asset'].browse(asset_id)
                    
                    if asset.exists():
                        # ¡INYECCIÓN! 
                        # Reemplazamos la celda vacía con el valor real del activo
                        line['columns'][method_period_index]['name'] = asset.method_period
                        line['columns'][method_period_index]['no_format'] = asset.method_period
                except Exception as e:
                    # Si falla al parsear el ID (por ej. si es una línea de total), saltamos
                    continue
                    
        return res