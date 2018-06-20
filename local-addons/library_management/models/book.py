# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char('Title')
    active = fields.Boolean(default=True)
    date_of_edition = fields.Date('Date of Edition')
    state = fields.Selection([('available', 'Available'),
                              ('borrowed', 'Borrowed'),
                              ('lost', 'Lost'),
                              ('unavailable', 'Unavailable')],
                             'State',
                             default='available')
    
    authors = fields.Many2many('res.partner',
                              string='Authors',
                              ondelete='restrict')
    editor = fields.Many2one('res.partner',
                             string='Editor',
                             ondelete='restrict')
    isbn = fields.Char("ISBN")
    cover = fields.Binary("Cover picture",
                          attachment=True)
    rental_history = fields.One2many('library.rental',
                                     inverse_name='book',
                                     string='Rental history')
    
    @api.multi
    def do_rent(self, contact):
        for record in self:
            record.state = 'borrowed'
            rental = {
                'book': record.id,
                #'customer': customer
            }
            self.env['library.rental'].create(rental)
    
    @api.multi
    def do_return(self):
        for record in self:
            record.state = 'available'

            rental = self.env['library.rental']
            this_rental = rental.search([('book', '=', record.id),
                                         ('date_returned', '=', False)])
            this_rental.ensure_one()
            this_rental.date_returned = fields.Date.today()
