from odoo import models, fields, api

class NoteWizard(models.TransientModel):
    _name = 'custom_reports.note_wizard'
    _description = 'Note Wizard'

    description = fields.Text(string='Descripción')

    def action_save_note(self):

        model_name = self.env.context.get('model_name')
        model_id = self.env.context.get('model_id')

        if model_name and model_id:
            model = self.env[model_name]
            record = model.browse(model_id)
            record.custom_note = self.description

        return {'type': 'ir.actions.act_window_close'}