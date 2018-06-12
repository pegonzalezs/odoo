{
    'name': 'The Citadel',
    'summary': 'Manage the training of future maesters.',
    'description': """* Create and edit classes, with different levels.
                      * Handle different sessions given by different maesters at different moments. 
                      * Register attendees of those sessions.
                      * Differentiate the sessions in preparation from the ones that will actually be given.
                      * Archive sessions.""",
    'author': 'Antoine Guenet',
    'license': 'AGPL-3',
    'website': 'http://www.odoo.com',
    'category': 'Events',
    'version': '11.0.1.0.0',
    'depends': ['base'],
    'application': True,
    'data': ['views/citadel.xml']
}
