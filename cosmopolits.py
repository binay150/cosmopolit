# -*- coding: utf-8; Mode: python; tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
# ex: set softtabstop=4 tabstop=4 shiftwidth=4 expandtab fileencoding=utf-8:

"""
Module which handles instantiation and configuration of the Sputnik Flask app
"""

# standard library
import os

# third party packages
from flask import Flask, session
from werkzeug.wsgi import SharedDataMiddleware

# local libraries
from Configuration import Configuration
from Constants import Constants
from Log import Log

# managers

from managers import ManageNewspapers

app = Flask('cosmopolits')

app._logger = Log.getLogger('cosmopolits')
app.logger_name = "cosmopolits"

# set up managers
class __ManagerContainer:
    pass
app.managers = __ManagerContainer()




# instantiate managers
app.managers.papers = ManageNewspapers()


# TODO - these static assets should be getting served by NGINX
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/static': os.path.join(os.path.dirname(__file__), 'static'),
    '/bootstrap': os.path.join(os.path.dirname(__file__), 'static'),
    '/app': os.path.join(os.path.dirname(__file__), 'app')
})

# blueprints and views
from blueprints.main import main
app.register_blueprint(main)
# blueprints and views
from blueprints.admin import admin
app.register_blueprint(admin, url_prefix='/admin')
#app.available_countries = available_countries
