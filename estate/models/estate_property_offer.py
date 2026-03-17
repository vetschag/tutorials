from odoo import fields, models, api
from datetime import date, timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ], string = 'Status',copy=False)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline') 
    partner_id = fields.Many2one('res.partner', string = "Partner", required=True)

    property_id = fields.Many2one('estate.property', string = "Property", required=True)

    @api.depends('validity', 'create_date') 
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else date.today()
            record.date_deadline = base_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else date.today()
            if record.date_deadline:
                record.validity = (record.date_deadline - base_date).days

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True
    
    def action_refused(self):
        for record in self:
            record.status = "refused"
        return True 
    
