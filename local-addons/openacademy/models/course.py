# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char('Title',
                       required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users',
                                     ondelete='set null',
                                     string='Responsible',
                                     index=True)
    
    session_ids = fields.One2many('openacademy.session',
                                  'course_id')

#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
