import logging
import re
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
NotAuthorized = logic.NotAuthorized

class CountryController(base.BaseController):
    pass
