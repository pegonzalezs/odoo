from odoo import models, fields

class CitadelCourse(models.Model):
    _name = 'citadel.course'
    _description = 'Citadel Course'
    
    name = fields.Char('Title', requried=True)
    state = fields.Selection([('draft', 'In preparation'),
                              ('ready', 'Ready')],
                             'State')
    level = fields.Selection([('novice', 'Novice'),
                              ('intermediate', 'Intermediate'),
                              ('expert', 'Expert'),
                              ('god', 'God')],
                             'Level')

    maester = fields.Many2one('res.partner',
                              string='Maester',
                              ondelete='set null')

    sessions = fields.One2many('citadel.session',
                               inverse_name='course',
                               string='Sessions')
