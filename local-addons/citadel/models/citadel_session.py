from odoo import models, fields

class CitadelSession(models.Model):
    _name = 'citadel.session'
    _description = 'Citadel Session'
    
    
    time_event = fields.Datetime('Time of the session')

    course = fields.Many2one('citadel.course',
                             string='Course',
                             ondelete='cascade')
    attendees = fields.Many2many('res.partner',
                                 string='Attendees')