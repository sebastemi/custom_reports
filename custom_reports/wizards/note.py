from odoo import models, fields, api

class NoteWizard(models.TransientModel):
    _name = 'custom_reports.note_wizard'
    _description = 'Note Wizard'

    description = fields.Text(string='Descripción')

    def action_save_note(self):
        pass