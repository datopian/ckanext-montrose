import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.plugins as lib_plugins
import ckanext.montrose.helpers as montrose_helpers
from ckan.controllers.package import (PackageController,
                                      url_with_params,
                                      _encode_params)

import logging
from urllib import urlencode
from datetime import datetime

from pylons import config
from paste.deploy.converters import asbool

import ckan.logic as logic
import ckan.lib.base as base
import ckan.lib.maintain as maintain
import ckan.lib.helpers as h
import ckan.model as model
import ckan.lib.render

from ckan.common import OrderedDict, _, json, request, c, g, response

log = logging.getLogger(__name__)

render = base.render
abort = base.abort
redirect = base.redirect

NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
check_access = logic.check_access
get_action = logic.get_action
tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
parse_params = logic.parse_params
flatten_to_string_key = logic.flatten_to_string_key

lookup_package_plugin = ckan.lib.plugins.lookup_package_plugin

class MontrosePlugin(plugins.SingletonPlugin, lib_plugins.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IResourceView, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IFacets, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'montrose')

    def before_map(self, map_):
        controller = 'ckanext.montrose.controllers.dashboard:DashboardsController'

        map_.connect('/kenya', controller=controller, action='kenya')

        return map_

    def get_helpers(self):
        return {
            'montrose_get_newly_released_data':
                montrose_helpers.montrose_get_newly_released_data,
            'montrose_convert_time_format':
                montrose_helpers.montrose_convert_time_format,
            'montrose_replace_or_add_url_param':
                montrose_helpers.montrose_replace_or_add_url_param
        }
        
class MontroseCountryPlugin(plugins.SingletonPlugin, lib_plugins.DefaultOrganizationForm):

    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IGroupForm, inherit=True)
    p.implements(p.IConfigurer)

    ## IRoutes

    def before_map(self, map):
        country_controller = 'ckanext.montrose.controllers.country:CountryController'
        with SubMapper(map, controller=country_controller) as m:
            # TODO: add route mappings
            pass

        return map

    ## IGroupForm

    def is_fallback(self):
        return True

    def group_types(self):
        return ['country']

    def form_to_db_schema_options(self, options):
        ''' This allows us to select different schemas for different
        purpose eg via the web interface or via the api or creation vs
        updating. It is optional and if not available form_to_db_schema
        should be used.
        If a context is provided, and it contains a schema, it will be
        returned.
        '''
        schema = options.get('context', {}).get('schema', None)
        if schema:
            return schema

        if options.get('api'):
            if options.get('type') == 'create':
                return self.form_to_db_schema_api_create()
            else:
                return self.form_to_db_schema_api_update()
        else:
            return self.form_to_db_schema()

    def form_to_db_schema_api_create(self):
        schema = super(MontroseCountry, self).form_to_db_schema_api_create()
        schema = self._modify_group_schema(schema)
        return schema

    def form_to_db_schema_api_update(self):
        schema = super(MontroseCountry, self).form_to_db_schema_api_update()
        schema = self._modify_group_schema(schema)
        return schema

    def form_to_db_schema(self):
        schema = super(MontroseCountry, self).form_to_db_schema()
        schema = self._modify_group_schema(schema)
        return schema

    def _modify_group_schema(self, schema):

        # Import core converters and validators
        # _convert_to_extras = p.toolkit.get_converter('convert_to_extras')
        # _ignore_missing = p.toolkit.get_validator('ignore_missing')

        default_validators = []
        schema.update({
            'montrose_country_header': [default_validators],
            'montrose_country_footer': [default_validators],
            'montrose_country_copyright': [default_validators],
            'montrose_datasets_per_page': [default_validators],
            'montrose_charts': [],
        })

        return schema

    def db_to_form_schema(self):

        # Import core converters and validators
        # _convert_from_extras = p.toolkit.get_converter('convert_from_extras')
        # _ignore_missing = p.toolkit.get_validator('ignore_missing')
        # _ignore = p.toolkit.get_validator('ignore')
        # _not_empty = p.toolkit.get_validator('not_empty')

        schema = super(MontroseCountry, self).form_to_db_schema()

        default_validators = []
        schema.update({
            'montrose_country_header': [default_validators],
            'montrose_country_footer': [default_validators],
            'montrose_country_copyright': [default_validators],
            'montrose_datasets_per_page': [default_validators],
            'montrose_charts': [],
        })

        return schema

    # IConfigurer
    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')