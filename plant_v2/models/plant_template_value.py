from odoo import models, fields


class PlantTemplateValue(models.Model):
    _name = "plant.template.value"
    _description = "Template Wert"

    template_id = fields.Many2one(
        "plant.template", string="Template",
        ondelete="cascade", required=True
    )
    field_id = fields.Many2one(
        "plant.field", string="Feld",
        ondelete="cascade", required=True
    )

    # Felder für die verschiedenen Typen
    value_text = fields.Char(string="Wert (Text)")
    value_image = fields.Binary(string="Wert (Bild)")
    value_selection_id = fields.Many2one(
        "plant.selection", string="Wert (Auswahl)",
        domain="[('field_id', '=', field_id)]"
    )

    # Computed Felder für einfachen Zugriff im Widget
    field_name = fields.Char(related="field_id.name", store=True)
    field_type = fields.Selection(related="field_id.field_type", store=True)
    type_id = fields.Many2one(related="field_id.type_id", store=True)
    aggregate_id = fields.Many2one(related="field_id.type_id.aggregate_id", store=True)
    block_id = fields.Many2one(related="field_id.type_id.aggregate_id.block_id", store=True)
