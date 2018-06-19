# -*- coding: utf-8 -*-

from odoo import models, fields

class LibraryRental(models.Model):
    _name = 'library.rental'
    _description = 'Library Rental'

    active = fields.Boolean(default=True)
    date_borrowed = fields.Date('Borrowed on',
                                default=fields.Date.today())
    date_returned = fields.Date('Returned on')

    book = fields.Many2one('library.book',
                           string='Book',
                           ondelete='cascade')
    customer = fields.Many2one('res.partner',
                               string='Customer',
                               ondelete='restrict')
