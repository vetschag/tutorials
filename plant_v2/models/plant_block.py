from odoo import models, fields


class PlantBlock(models.Model):
    _name = "plant.block"
    _description = "Block"

    name = fields.Char(string="Name", required=True)
    # Block gehört zur Plant — nicht zum Template!
    plant_id = fields.Many2one("plant.plant", string="Plant", ondelete="cascade")
    aggregate_ids = fields.One2many("plant.aggregate", "block_id", string="Aggregate")
