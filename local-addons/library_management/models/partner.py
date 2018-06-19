# -*- coding: utf-8 -*-

from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    books_rented = fields.One2many('library.rental',
                                   inverse_name='customer',
                                   string='Rented books')
    books_authored = fields.Many2many('library.book',
                                      string='Authored books')
    books_edited = fields.One2many('library.book',
                                   inverse_name='editor',
                                   string='Edited books')
