from odoo import models, fields


class PlantSelection(models.Model):
    _name = "plant.selection"
    _description = "Auswahloption"

    name = fields.Char(string="Name", required=True)
    field_id = fields.Many2one("plant.field", string="Feld", ondelete="cascade")
                