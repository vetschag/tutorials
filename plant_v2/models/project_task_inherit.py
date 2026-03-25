from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = "project.task"

    plant_template_id = fields.Many2one(
        "plant.template",
        string="Plant Template",
        ondelete="set null",
    )

    def action_view_plant_template(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Plant Template",
            "res_model": "plant.template",
            "view_mode": "form",
            "res_id": self.plant_template_id.id,
        }
