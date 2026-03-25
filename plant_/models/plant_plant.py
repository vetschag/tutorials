from odoo import models, fields


class PlantPlant(models.Model):
    _name = "plant.plant"
    _description = "Plant"

    name = fields.Char(string="Name", required=True)
    template_ids = fields.One2many("plant.template", "plant_id", string="Templates")
