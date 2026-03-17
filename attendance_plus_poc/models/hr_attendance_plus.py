from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrAttendance(models.Model):
    _inherit = "hr.attendance"  # Wir erweitern das bestehende Modell

    # Neue Felder für PoC
    project_id = fields.Many2one("project.project", string="Projekt")
    task_id = fields.Many2one("project.task", string="Task")

    @api.constrains('check_out')
    def _check_project_selected(self):
        """Sicherstellen, dass vor dem Ausstempeln ein Projekt gewählt wird"""
        for att in self:
            if att.check_out and not att.project_id:
                raise ValidationError("Projekt muss vor dem Ausstempeln gewählt werden.")

    def action_check_out(self):
        """Beim Ausstempeln automatisch Timesheet erzeugen"""
        res = super().action_check_out()

        for att in self:
            if att.project_id and att.task_id and att.check_out:
                # Dauer in Stunden
                duration = (att.check_out - att.check_in).total_seconds() / 3600

                # Timesheet erstellen
                self.env["account.analytic.line"].create({
                    "name": f"Auto Timesheet von Attendance {att.check_in}",
                    "employee_id": att.employee_id.id,
                    "project_id": att.project_id.id,
                    "task_id": att.task_id.id,
                    "unit_amount": duration,
                })

        return res
