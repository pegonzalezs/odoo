# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char('Title',
                       required=True)
    active = fields.Boolean(default=True)
    start_date = fields.Date('Start Date',
                             default=fields.Date.today())
    duration = fields.Float("Duration",
                            digits=(6, 2),
                            help="Duration in days")
    seats = fields.Integer('Number of Seats')
    instructor_id = fields.Many2one('res.partner',
                                    ondelete='set null',
                                    domain=['|', 
                                                ('instructor', '=', True),
                                                ('category_id.name', 'ilike', 'teacher')],
                                    string='Instructor')
    course_id = fields.Many2one('openacademy.course',
                                required=True,
                                ondelete='cascade',
                                string='Course')
    attendee_ids = fields.Many2many('res.partner',
                                    string='Attendees')
    taken_seats = fields.Float('Taken seats',
                               compute='_taken_seats')
    
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for record in self:
            if not record.seats:
                record.taken_seats = 0.
            else:
                pc = 100 * (len(record.attendee_ids) / record.seats)
                record.taken_seats = pc

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative"
                }
            }
        if len(self.attendee_ids) > self.seats:
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees"
                }
            }
    
    @api.constrains('instructor_id', 'attendee_ids')
    def _verify_instructor_not_in_attendees(self):
        for record in self:
            if record.instructor_id in record.attendee_ids:
                raise ValidationError("An instructor cannot be a student at his own session.")
