from odoo import models, fields


class PlantAggregate(models.Model):
    _name = "plant.aggregate"
    _description = "Aggregat"

    name = fields.Char(string="Name", required=True)
    block_id = fields.Many2one("plant.block", string="Block", ondelete="cascade")
    type_ids = fields.One2many("plant.type", "aggregate_id", string="Typen")
