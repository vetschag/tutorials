from odoo import models, fields


class PlantBlock(models.Model):
    _name = "plant.block"
    _description = "Block"

    name = fields.Char(string="Name", required=True)
    template_id = fields.Many2one("plant.template", string="Template", ondelete="cascade")
    aggregate_ids = fields.One2many("plant.aggregate", "block_id", string="Aggregate")
