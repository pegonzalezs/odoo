# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta

class Volunteer(models.Model):
    _name = 'coop.volunteer'

    name = fields.Char("Name", required=True)
    availability = fields.Selection([('recurrent', "Recurring Tasks"),
                                     ('punctual', "Every now and then")],
                                    "Availability")
    tasks = fields.Many2many('coop.task',
                             string="Tasks")

class Task(models.Model):
    _name = 'coop.task'

    name = fields.Char("Name", required=True)
    state = fields.Selection([('todo', "To do"),
                              ('progress', "In progres"),
                              ('done', "Done")],
                             "State")
    task_type = fields.Selection([('recurring', "Recurring"),
                                  ('punctual', "Punctual")])
    start_time = fields.Datetime("Start time")
    end_time = fields.Datetime("End time")
    duration = fields.Float("Duration in hours",
                            compute='_get_duration',
                            inverse='_set_duration')
    day_nr = fields.Many2one('coop.day',
                             "Day number")
    required_workforce = fields.Integer("Volunteers Required")
    workers = fields.Many2many('coop.volunteer',
                               string="Assigned workers")
    
    @api.depends('start_time', 'end_time')
    def _get_duration(self):
        for r in self:
            if r.end_time and r.start_time:
                end = fields.Datetime.from_string(r.end_time)
                start = fields.Datetime.from_string(r.start_time)
                duration = end - start
                r.duration = duration.total_seconds() / 60 / 60
    
    @api.depends('duration', 'start_time')
    def _set_duration(self):
        for r in self:
            if r.start_time and r.duration:
                start = fields.Datetime.from_string(r.start_time)
                r.end_time = start + timedelta(hours=r.duration)

class WorkDay(models.Model):
    _name = 'coop.day'

    day_nr = fields.Integer("Number", required=True)
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
    