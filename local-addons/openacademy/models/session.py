# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char('Title',
                       required=True)
    start_date = fields.Date('Start Date')
    duration = fields.Float("Duration",
                            digits=(6, 2),
                            help="Duration in days")
    seats = fields.Integer('Number of Seats')
