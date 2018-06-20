# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Contact(models.Model):
    _inherit = 'res.partner'

    books_rented = fields.One2many('library.rental',
                                   inverse_name='customer',
                                   string='Rented books')
    books_authored = fields.Many2many('library.book',
                                      string='Authored books')
    books_edited = fields.One2many('library.book',
                                   inverse_name='editor',
                                   string='Edited books')

    is_author = fields.Boolean("Author", compute="_is_author", store=True)
    is_editor = fields.Boolean("Editor", compute="_is_editor", store=True)
    is_customer = fields.Boolean("Customer", compute="_is_customer", store=True)

    @api.depends('books_authored')
    def _is_author(self):
        for r in self:
            r.is_author = len(r.books_authored) > 0
    
    @api.depends('books_edited')
    def _is_editor(self):
        for r in self:
            r.is_editor = len(r.books_edited) > 0
    
    @api.depends('books_rented')
    def _is_customer(self):
        for r in self:
            r.is_customer = len(r.books_rented) > 0
