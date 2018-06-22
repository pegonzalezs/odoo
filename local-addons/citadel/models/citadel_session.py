from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CitadelSession(models.Model):
    _name = 'citadel.session'
    _description = "Citadel Session"

    active = fields.Boolean(default=True)
    state = fields.Selection([('draft', "In preparation"),
                              ('ready', "Ready")],
                             "State")
    time_event = fields.Datetime("Time of the session")
    max_attendees = fields.Integer("Maximum number of Attendees")
    completion_pc = fields.Float("Percentage of seats taken",
                                   compute='_get_completion_pc',
                                   readonly=True)

    course = fields.Many2one('citadel.course',
                             string="Course",
                             ondelete='cascade')
    attendees = fields.Many2many('res.partner',
                                 string="Attendees")
    
    @api.constrains('max_attendees', 'attendees')
    def _check_max_attendees(self):
        if len(self.attendees) > self.max_attendees:
            raise ValidationError("Too many attendees: either remove an attendee or raise the maximum number of attendees.")

    @api.depends('max_attendees', 'attendees')
    def _get_completion_pc(self):
        for r in self:
            r.completion_pc = 100 * (float(len(r.attendees))/r.max_attendees)
