from odoo import models, fields


class PlantType(models.Model):
    _name = "plant.type"
    _description = "Typ"

    name = fields.Char(string="Name", required=True)
    aggregate_id = fields.Many2one("plant.aggregate", string="Aggregat", ondelete="cascade")
    field_ids = fields.One2many("plant.field", "type_id", string="Felder")
