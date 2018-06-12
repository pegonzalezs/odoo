from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    position = fields.Selection([('maester', 'Maester'),
                                 ('trainee', 'Trainee'),
                                 ('unknown', 'Unknown')],
                                'Position')
    courses_taught = fields.One2many('citadel.course',
                                     inverse_name='maester',
                                     string='Courses taught')
    