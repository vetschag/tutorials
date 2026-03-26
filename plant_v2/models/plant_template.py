from odoo import models, fields, api


class PlantTemplate(models.Model):
    _name = "plant.template"
    _description = "Plant Template"

    name = fields.Char(string="Name", required=True)
    plant_id = fields.Many2one("plant.plant", string="Plant", required=True)
    state = fields.Selection([
        ("draft", "Entwurf"),
        ("active", "Aktiv"),
        ("done", "Abgeschlossen"),
    ], default="draft", string="Status")

    value_ids = fields.One2many(
        "plant.template.value", "template_id", string="Werte"
    )

    # Verknüpfung zu Project Tasks
    task_ids = fields.One2many(
        "project.task", "plant_template_id", string="Tasks"
    )
    task_count = fields.Integer(compute="_compute_task_count")

    def _compute_task_count(self):
        for rec in self:
            rec.task_count = len(rec.task_ids)

    def action_view_tasks(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Tasks",
            "res_model": "project.task",
            "view_mode": "list,form",
            "domain": [("plant_template_id", "=", self.id)],
            "context": {"default_plant_template_id": self.id},
        }

    def action_download_docx(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": f"/plant/template/{self.id}/docx",
            "target": "new",
        }

    def action_generate_values(self):
        self.ensure_one()
        if not self.plant_id:
            return
        self.value_ids.unlink()
        fields_to_create = []
        for block in self.plant_id.block_ids:
            for aggregate in block.aggregate_ids:
                for type_ in aggregate.type_ids:
                    for field in type_.field_ids:
                        fields_to_create.append({
                            "template_id": self.id,
                            "field_id": field.id,
                        })
        if fields_to_create:
            self.env["plant.template.value"].create(fields_to_create)
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Struktur geladen",
                "message": f"{len(fields_to_create)} Felder wurden erstellt.",
                "type": "success",
            },
        }

    @api.model_create_multi
    def create(self, vals_list):
        templates = super().create(vals_list)
        for template in templates:
            if template.plant_id:
                template.action_generate_values()
        return templates
