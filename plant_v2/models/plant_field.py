from odoo import models, fields


class PlantField(models.Model):
    _name = "plant.field"
    _description = "Feld Definition"

    name = fields.Char(string="Name", required=True)
    type_id = fields.Many2one("plant.type", string="Typ", ondelete="cascade")
    field_type = fields.Selection([
        ("text", "Text"),
        ("image", "Image"),
        ("selection", "Selection"),
    ], string="Feldtyp", required=True)

    # NUR Struktur — KEINE Werte mehr hier!
    selection_ids = fields.One2many("plant.selection", "field_id", string="Auswahloptionen")
