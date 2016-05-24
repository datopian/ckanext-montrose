import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.base as base
from datetime import date, datetime

from logging import getLogger

logger = getLogger(__name__)

class MontrosePlugin(plugins.SingletonPlugin):
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

    def after_map(self, map_):
        controller = 'ckanext.montrose.plugin:DashboardsController'

        map_.connect('/kenya', controller=controller, action='kenya')

        return map_

    def get_helpers(self):
        return {
            'montrose_get_newly_released_data':
                montrose_get_newly_released_data
        }



class DashboardsController(base.BaseController):
    def kenya(self):
        '''map_resource_view_id = '882d4d34-895b-4ff2-8f41-2ba916665734'
        data_dict = {
            'id': map_resource_view_id
        }
        map_resource_view = toolkit.get_action('resource_view_show')({}, data_dict)

        data_dict = {
            'id': map_resource_view['resource_id']
        }
        map_resource = toolkit.get_action('resource_show')({}, data_dict)

        data_dict = {
            'id': map_resource['package_id']
        }
        map_package = toolkit.get_action('package_show')({}, data_dict)

        extra = {'map_package': map_package,
                 'map_resource': map_resource,
                 'map_resource_view': map_resource_view}

        return plugins.toolkit.render('dashboards/kenya.html', extra_vars=extra)'''

        ids = ['f111fa89-44f3-47d8-a584-eecbea046cd8',
               'db91e252-43a6-4520-958c-f226a0acedad',
               'f0186ced-847c-4367-88f0-d5641bf0117e',
               '0a844f3b-a0a4-4ba1-af07-302607105b3e',
               '015abce5-7102-4457-b912-861491bef523',
               'd97f098f-37fe-4ec5-a058-6bb41bcb28d0']

        charts = []
        for id in ids:
            charts.append(get_resourceview_resource_package(id))

        return plugins.toolkit.render('dashboards/kenya.html', extra_vars={'charts': charts})


def get_resourceview_resource_package(resource_view_id):
    data_dict = {
        'id': resource_view_id
    }
    resource_view = toolkit.get_action('resource_view_show')({}, data_dict)

    data_dict = {
        'id': resource_view['resource_id']
    }
    resource = toolkit.get_action('resource_show')({}, data_dict)

    data_dict = {
        'id': resource['package_id']
    }
    package = toolkit.get_action('package_show')({}, data_dict)

    return [resource_view, resource, package]


def montrose_get_newly_released_data(limit=5):
    try:
        pkg_search_results = toolkit.get_action('package_search')(data_dict={
            'sort': 'metadata_modified desc',
            'rows': limit,
        })['results']

    except toolkit.ValidationError, search.SearchError:
        return []
    else:
        pkgs = []
        for pkg in pkg_search_results:
            package = toolkit.get_action('package_show')(data_dict={
                'id': pkg['id']
            })
            modified = datetime.strptime(package['metadata_modified'].split('T')[0], '%Y-%m-%d')
            package['human_metadata_modified'] = modified.strftime("%d %B %Y")
            pkgs.append(package)
        return pkgs
