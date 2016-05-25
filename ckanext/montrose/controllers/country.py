import logging
from pylons import config

import ckan.plugins as p
import ckan.plugins.toolkit as t
import ckan.lib.plugins as lib_plugins
from ckan.controllers.organization import OrganizationController

import ckan.logic as logic
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.model as model
import ckan.lib.render

from ckan.common import request, c, g, response

log = logging.getLogger(__name__)

render = base.render
abort = base.abort
redirect = base.redirect

class CountryController(OrganizationController, lib_plugins.DefaultOrganizationForm):
    
    def group_form(self):
        pass

    def setup_template_variables(self, context, data_dict):
        pass

    def new_template(self):
        pass

    def index_template(self):
        pass

    def edit_template(self):
        pass