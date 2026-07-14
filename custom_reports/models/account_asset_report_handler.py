from odoo import models

class AccountAssetReportHandler(models.AbstractModel):
    # Heredamos el gestor personalizado exacto del reporte de depreciación
    _inherit = 'account.asset.report.handler'

    def _custom_line_dict(self, options, line_id, current_groupby, record, level):
        """
        Interceptamos la construcción de la línea.
        Este es el diccionario que Odoo envía finalmente a la interfaz gráfica.
        """
        # 1. Ejecutamos el código original para que Odoo arme la línea normal
        res = super()._custom_line_dict(options, line_id, current_groupby, record, level)
        
        # 2. Verificamos que estamos en una línea de activo real (no en un total o cabecera)
        # En Odoo 17, el 'record' en este punto suele ser el objeto account.asset
        if record and record._name == 'account.asset':
            
            res['method_number'] = record.method_number
            
        return res