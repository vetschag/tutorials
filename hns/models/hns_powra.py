from odoo import models, fields, api


class HnsPowra(models.Model):
    _name = "hns.powra"
    _description = "POWRA Point of Work Risk Analysis App "

    name = fields.Char("Titel", default="POWRA Formular")

    

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


    @api.onchange('q1_yes')
    def _onchange_q1_yes(self):
            if self.q1_yes:
                self.q1_no = False

    @api.onchange('q1_no')
    def _onchange_q1_no(self):
        if self.q1_no:
            self.q1_yes = False
    
   
   



   