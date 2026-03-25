from odoo import models, fields


class PlantField(models.Model):
    _name = "plant.field"
    _description = "Feld"

    name = fields.Char(string="Name", required=True)
    type_id = fields.Many2one("plant.type", string="Typ", ondelete="cascade")

    field_type = fields.Selection([
        ("text", "Text"),
        ("image", "Image"),
        ("selection", "Selection"),
    ], string="Feldtyp", required=True)

    # Werte je nach Feldtyp
    value_text = fields.Char(string="Wert (Text)")
    value_image = fields.Binary(string="Wert (Bild)")
    value_selection = fields.Many2one("plant.selection", string="Wert (Auswahl)")

    # Verfügbare Optionen für Selection-Felder
    selection_ids = fields.One2many("plant.selection", "field_id", string="Auswahloptionen")
