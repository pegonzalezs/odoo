# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Volunteer(models.Model):
    _name = 'coop.volunteer'

    name = fields.Char("Name")
    availability = fields.Selection([('recurrent', "Recurring Tasks"),
                                     ('punctual', "Every now and then")],
                                    "Availability")

class Task(models.Model):
    _name = 'coop.task'

    name = fields.Char("Name")
    state = fields.Selection([('todo', "To do"),
                              ('progress', "In progres"),
                              ('done', "Done")],
                             "State")
    required_workforce = fields.Integer("Volunteers Required")

class WorkDay(models.Model):
    _name = 'coop.day'

    task_ids = fields.Many2many('coop.task',
                                string="Tasks")
    volunteer_ids = fields.Many2many('coop.volunteer',
                                     string="Volunteers")
    
    required_workforce = fields.Integer("Volunteers Required",
                                        compute='_required_workforce')
    
    @api.depends('task_ids')
    def _required_workforce(self):
        for r in self:
            for task in r.task_ids:
                r.required_workforce += task.required_workforce
    