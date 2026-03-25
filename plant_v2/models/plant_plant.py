from odoo import models, fields


class PlantPlant(models.Model):
    _name = "plant.plant"
    _description = "Plant"

    name = fields.Char(string="Name", required=True)

    # Struktur direkt an Plant hängen
    block_ids = fields.One2many("plant.block", "plant_id", string="Blöcke")
    template_ids = fields.One2many("plant.template", "plant_id", string="Templates")
    template_count = fields.Integer(compute="_compute_template_count")

    def _compute_template_count(self):
        for rec in self:
            rec.template_count = len(rec.template_ids)
