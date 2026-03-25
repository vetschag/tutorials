from odoo import models, fields


class PlantTemplate(models.Model):
    _name = "plant.template"
    _description = "Plant Template"

    name = fields.Char(string="Name", required=True)
    plant_id = fields.Many2one("plant.plant", string="Plant")
    block_ids = fields.One2many("plant.block", "template_id", string="Blöcke")
    state = fields.Selection([
        ("active", "Aktiv"),
        ("draft", "Entwurf"),
        ("done", "Abgeschlossen"),
    ], default="active", string="Status")
