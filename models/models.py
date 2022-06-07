# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class video_club(models.Model):
#     _name = 'video_club.video_club'
#     _description = 'video_club.video_club'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


import logging



from dataclasses import field
from email.policy import default
import datetime
#from typing_extensions import Required

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date
from odoo.tools.translate import _
logger = logging.getLogger(__name__)
#from odoo import typing_extensions


class movie (models.Model):
    
    _name='video.movie'
    _description='peliculas que posee el videoclub'
    


    name = fields.Char(string='título', required=True)
    category_id = fields.Many2one('video.movie.category', string='Genero')
    synopsis = fields.Text(string='sinopsis')
    director = fields.Char(string='director')
    releaseDate = fields.Date('Fecha Prestamo',Required=True,default=fields.date.today())
    state = fields.Selection([
        ('draft', 'Unavailable'),
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost')],
        'State', default="draft")

    cover= fields.Binary(string='portada')

    
   


    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'borrowed'),
                   ('borrowed', 'available'),
                   ('available', 'lost'),
                   ('borrowed', 'lost'),
                   ('lost', 'available')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for movie in self:
            if movie.is_allowed_transition(movie.state, new_state):
                movie.state = new_state
            else:
                message = _('Moving from %s to %s is not allowed') % (movie.state, new_state)
                raise UserError(message)

    def make_available(self):
        self.change_state('available')

    def make_borrowed(self):
        self.change_state('borrowed')

    def make_lost(self):
        self.change_state('lost')

    def log_all_videoClub_members(self):
        library_member_model = self.env['video.member']  # This is an empty recordset of model library.member
        all_members = library_member_model.search([])
        print("ALL MEMBERS:", all_members)
        return True


    def create_categories(self):
        categ1 = {
            'name': 'Child category 1',
            'description': 'Description for child 1'
        }
        categ2 = {
            'name': 'Child category 2',
            'description': 'Description for child 2'
        }
        parent_category_val = {
            'name': 'Parent category',
            'description': 'Description for parent category',
            'child_ids': [
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }
        # Total 3 records (1 parent and 2 child) will be craeted in library.book.category model
        record = self.env['video.movie.category'].create(parent_category_val)
        return True

    def change_release_date(self):
        self.ensure_one()
        self.releaseDate = fields.Date.today()


    def find_movie(self):
        domain = [
            '|',
                '&', ('name', 'ilike', 'Book Name'),
                     ('category_id.name', '=', 'Category Name'),
                '&', ('name', 'ilike', 'Book Name 2'),
                     ('category_id.name', '=', 'Category Name 2')
        ]
        movies = self.search(domain)
        logger.info('Movie found: %s', movies)
        return True




    
    
    
    
       
class VideoClubClient(models.Model):

    _name = 'video.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = "video member"

    partner_id = fields.Many2one('res.partner', ondelete='cascade',string='nombre')
    date_start = fields.Date('Cliente desde')
    date_end = fields.Date('Fecha fin')
    member_number = fields.Char('member Number')
    date_of_birth = fields.Date('Date of birth')
    clientPhotography= fields.Binary()
    dni=fields.Integer(string='DNI (sin letra)')
    
    @api.depends("dni")
    def _calculate_member_number(self):
        self.member_number=self.dni//2


class VideoClubEmployees(models.Model):
    _name = 'video.employee'
    _inherits = {'res.partner': 'partner_id'}
    _description = "videoClub employee"


    partner_id = fields.Many2one('res.partner', ondelete='cascade',string='nombre',required=True)

    date_start = fields.Date('Empleado desde')
    date_end = fields.Date('Fecha fin')
    employee_number = fields.Integer(compute="_compute_number",string='Nº empleado',store=True)
    date_of_birth = fields.Date('fecha de nacimiento')
    employeePhotografy= fields.Binary()
    nss=fields.Integer(string='Nº seguridad Social')

    @api.depends("nss")
    def _compute_number(self):
        for record in self:
            self.employee_number = self.nss//2 
    


     
    







