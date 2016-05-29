import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.plugins as lib_plugins
import ckanext.montrose.helpers as montrose_helpers

from routes.mapper import SubMapper
from pylons import config

log = logging.getLogger(__name__)

class MontrosePlugin(plugins.SingletonPlugin, lib_plugins.DefaultOrganizationForm):
    
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IGroupForm, inherit=True)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IFacets, inherit=True)

    ## IRoutes

    def before_map(self, map):

        map.redirect('/group/{url:.*}', '/country/{url}',
                     _redirect_code='301 Moved Permanently')
        map.redirect('/group', '/country',
                     _redirect_code='301 Moved Permanently')
        map.redirect('/organization/{url:.*}', '/country/{url}',
                     _redirect_code='301 Moved Permanently')
        map.redirect('/organization', '/country',
                     _redirect_code='301 Moved Permanently')
        
        org_controller = 'ckan.controllers.organization:OrganizationController'
        with SubMapper(map, controller=org_controller) as m:
            m.connect('organization_index', '/country', action='index')
            m.connect('/country/list', action='list')
            m.connect('/country/new', action='new')
            m.connect('country_read', '/country/{id}', action='read')
            m.connect('country_activity', '/country/activity/{id}',
                      action='activity', ckan_icon='time')
            m.connect('country_edit', '/country/edit/{id}',
                      action='edit', ckan_icon='edit')
            
        # Define dashboard controller routes
        
        ctrl = 'ckanext.montrose.controllers.dashboard:DashboardsController'
        map.connect('/country/{name}/dashboard', controller=ctrl, 
                    action='montrose_country_dashboard')
            
        return map

    ## IGroupForm

    def is_fallback(self):
        return True
    
    def group_types(self):
        return ['organization']

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
        schema = super(MontrosePlugin, self).form_to_db_schema_api_create()
        schema = self._modify_group_schema(schema)
        return schema

    def form_to_db_schema_api_update(self):
        schema = super(MontrosePlugin, self).form_to_db_schema_api_update()
        schema = self._modify_group_schema(schema)
        return schema

    def form_to_db_schema(self):
        schema = super(MontrosePlugin, self).form_to_db_schema()
        schema = self._modify_group_schema(schema)
        return schema

    def _modify_group_schema(self, schema):

        # Import core converters and validators
        _convert_to_extras = toolkit.get_converter('convert_to_extras')
        _ignore_missing = toolkit.get_validator('ignore_missing')

        default_validators = [_ignore_missing,_convert_to_extras]
        schema.update({
            'montrose_country_header': default_validators,
            'montrose_country_footer': default_validators,
            'montrose_country_copyright': default_validators,
            'montrose_lang_is_active': default_validators,
            'montrose_dashboard_base_color': default_validators,
            'montrose_dashboard_is_active': default_validators,
            'montrose_datasets_per_page': default_validators,
            'montrose_charts': default_validators,
            'montrose_map': default_validators,
            'montrose_map_main_property': default_validators,
            'montrose_main_color': default_validators,
            'montrose_new_data_color': default_validators,
            'montrose_all_data_color': default_validators,
        })
        
        charts = {}
        for _ in range(1, 7):
            charts.update({'montrose_chart_{idx}'.format(idx=_): default_validators,
                          'montrose_chart_{idx}_subheader'.format(idx=_): default_validators})
            
        schema.update(charts)
        return schema

    def db_to_form_schema(self):

        # Import core converters and validators
        _convert_from_extras = toolkit.get_converter('convert_from_extras')
        _ignore_missing = toolkit.get_validator('ignore_missing')
        _ignore = toolkit.get_validator('ignore')
        _not_empty = toolkit.get_validator('not_empty')

        schema = super(MontrosePlugin, self).form_to_db_schema()

        default_validators = [_convert_from_extras, _ignore_missing]
        schema.update({
            'montrose_country_header': default_validators,
            'montrose_country_footer': default_validators,
            'montrose_country_copyright': default_validators,
            'montrose_lang_is_active': default_validators,
            'montrose_dashboard_base_color': default_validators,
            'montrose_dashboard_is_active': default_validators,
            'montrose_datasets_per_page': default_validators,
            'montrose_charts': default_validators,
            'montrose_map': default_validators,
            'montrose_map_main_property': default_validators,
            'montrose_main_color': default_validators,
            'montrose_new_data_color': default_validators,
            'montrose_all_data_color': default_validators,
            'num_followers': [_not_empty],
            'package_count': [_not_empty],
        })
        
        charts = {}
        for _ in range(1, 7):
            charts.update({'montrose_chart_{idx}'.format(idx=_): default_validators,
                          'montrose_chart_{idx}_subheader'.format(idx=_): default_validators})
            
        schema.update(charts)
        return schema
    
    ## IActions

    def get_actions(self):

        module_root = 'ckanext.montrose.logic.action'
        action_functions = _get_logic_functions(module_root)

        return action_functions

    def get_helpers(self):
        return {
            'montrose_get_newly_released_data':
                montrose_helpers.montrose_get_newly_released_data,
            'montrose_convert_time_format':
                montrose_helpers.montrose_convert_time_format,
            'montrose_replace_or_add_url_param':
                montrose_helpers.montrose_replace_or_add_url_param,
            'organization_list':
                montrose_helpers.organization_list,
            'get_org_chart_views':
                montrose_helpers.country_views.get_charts,
            'montrose_get_chart_resources':
                montrose_helpers.get_resourceview_resource_package,
            'get_org_map_views': 
                montrose_helpers.country_views.get_maps,
            'montrose_get_resource_url':
                montrose_helpers.montrose_get_resource_url,
            'montrose_get_geojson_properties': 
                montrose_helpers.montrose_get_geojson_properties
        }
        
    ## IConfigurer
    
    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_resource('fanstatic', 'montrose')
        toolkit.add_public_directory(config, 'public')
        
def _get_logic_functions(module_root, logic_functions = {}):
    module = __import__(module_root)
    for part in module_root.split('.')[1:]:
        module = getattr(module, part)

    for key, value in module.__dict__.items():
        if not key.startswith('_') and  (hasattr(value, '__call__')
                    and (value.__module__ == module_root)):
            logic_functions[key] = value
            
    return logic_functions
        
