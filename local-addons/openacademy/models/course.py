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
    
    _sql_constraints = [
        ('description_is_not_title',
         'CHECK (description != name)',
         "The description cannot be the same as the title"),
        ('name_unique',
         'UNIQUE (name)',
         "The name must be unique")
    ]

#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
