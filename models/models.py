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


logger = logging.getLogger(__name__)
from dataclasses import field
from email.policy import default
#from typing_extensions import Required

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
#from odoo import typing_extensions


class movie (models.Model):
    _name='video_club.pelicula'
    _description='peliculas que posee el videoclub'

    title = fields.Char(string='título')
    genre = fields.Many2one('Categories', string='Genre')
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
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                message = _('Moving from %s to %s is not allowd') % (book.state, new_state)
                raise UserError(message)

    def make_available(self):
        self.change_state('available')

    def make_borrowed(self):
        self.change_state('borrowed')

    def make_lost(self):
        self.change_state('lost')

    def log_all_library_members(self):
        library_member_model = self.env['library.member']  # This is an empty recordset of model library.member
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
        record = self.env['library.book.category'].create(parent_category_val)
        return True

    def change_release_date(self):
        self.ensure_one()
        self.date_release = fields.Date.today()

    def find_book(self):
        domain = [
            '|',
                '&', ('name', 'ilike', 'Book Name'),
                     ('category_id.name', '=', 'Category Name'),
                '&', ('name', 'ilike', 'Book Name 2'),
                     ('category_id.name', '=', 'Category Name 2')
        ]
        books = self.search(domain)
        logger.info('Books found: %s', books)
        return True

    
class VideoClubClient(models.Model):

    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = "Library member"

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char('member Number')
    date_of_birth = fields.Date('Date of birth')
    clientPhotography= fields.Binary()
    age = fields.Integer( string='age',compute='_compute_age', inverse='_inverse_age', search='_search_age',store=False,compute_sudo=True)



@api.depends('date_of_birth')

def _compute_age(self): 
    today = fields.Date.today() 
    for movie in self.filtered('date_of_birth'):
        if movie.date_of_birth: 
            delta = today - movie.date_of_birth
            movie.age = delta.days 
        else:
            movie.age = 0




class VideoClubEmployees(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = "VideoClub employee"

    partner_id = fields.Many2one( 'res.partner',
        string='Partner',
        ondelete='cascade',required=True)
        
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    employee_number = fields.Char(string='Nº empleado')
    date_of_birth = fields.Date('Date of birth')
    clientPhotography= fields.Binary()








