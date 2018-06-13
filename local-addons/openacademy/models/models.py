# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char('Title',
                       required=True)
    description = fields.Text()

class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char('Title',
                       required=True)
    start_date = fields.Date('Start Date')
    duration = fields.Float("Duration",
                            digits=(6, 2),
                            help="Duration in days")
    seats = fields.Integer('Number of Seats')
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100