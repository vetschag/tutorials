from odoo import models, fields, api
from datetime import date

class HnsLmra(models.Model):
    _name = "hns.lmra"
    _description = "LMRA Last Minute Risk Analyse App "

    name = fields.Char("Titel", compute="_compute_name", store=True)
    date = fields.Date(string="Datum", default=fields.Date.context_today)

    # 10 Ja/Nein-Fragen
    q1_yes = fields.Boolean("Ja")
    q1_no = fields.Boolean("Nein")
    q2_yes = fields.Boolean("Ja")
    q2_no = fields.Boolean("Nein")
    q3_yes = fields.Boolean("Ja")
    q3_no = fields.Boolean("Nein")
    q4_yes = fields.Boolean("Ja")
    q4_no = fields.Boolean("Nein")
    q5_yes = fields.Boolean("Ja")
    q5_no = fields.Boolean("Nein")
    q6_yes = fields.Boolean("Ja")
    q6_no = fields.Boolean("Nein")
    q7_yes = fields.Boolean("Ja")
    q7_no = fields.Boolean("Nein")
    q8_yes = fields.Boolean("Ja")
    q8_no = fields.Boolean("Nein")
    q9_yes = fields.Boolean("Ja")
    q9_no = fields.Boolean("Nein")
    q10_yes = fields.Boolean("Ja")
    q10_no = fields.Boolean("Nein")


    @api.onchange('q1_yes','q2_yes','q3_yes','q4_yes','q5_yes','q6_yes','q7_yes','q8_yes','q9_yes','q1_yes')
    def _onchange_q_yes(self):
        for record in self:
            if record.q1_yes:
                record.q1_no = False
            if record.q2_yes:
                record.q2_no = False
            if record.q3_yes:
                record.q3_no = False
            if record.q4_yes:
                record.q4_no = False
            if record.q5_yes:
                record.q5_no = False
            if record.q6_yes:
                record.q6_no = False
            if record.q7_yes:
                record.q7_no = False
            if record.q8_yes:
                record.q8_no = False
            if record.q9_yes:
                record.q9_no = False
            if record.q10_yes:
                record.q10_no = False


    @api.onchange('q1_no','q2_no','q3_no','q4_no','q5_no','q6_no','q7_no','q8_no','q9_no','q10_no')
    def _onchange_q_no(self):
        for record in self:
            if record.q1_no:
                record.q1_yes = False
            if record.q2_no:
                record.q2_yes = False
            if record.q3_no:
                record.q3_yes = False
            if record.q4_no:
                record.q4_yes = False
            if record.q5_no:
                record.q5_yes = False
            if record.q6_no:
                record.q6_yes = False
            if record.q7_no:
                record.q7_yes = False
            if record.q8_no:
                record.q8_yes = False
            if record.q9_no:
                record.q9_yes = False
            if record.q10_no:
                record.q10_yes = False

    
   
   
    def action_send(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hns.lmra',
            'view_mode': 'list,form',  # 'list' statt 'tree'
            'target': 'current',        # im gleichen Fenster öffnen
        }
    
    @api.depends('date')
    def _compute_name(self):
        for record in self:
            record.name = f"LMRA vom {record.date or date.today()}"