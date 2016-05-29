import logging
import json

from pylons import config
from ckan import logic

import ckan.plugins as p
import ckan.lib.helpers as h

from ckanext.montrose.helpers import _get_action, montrose_get_geojson_properties,\
                             get_resourceview_resource_package, montrose_get_resource_url,\
                             get_resource_resource_views

log = logging.getLogger(__name__)

@p.toolkit.side_effect_free
def montrose_show_datasets(context, data_dict):
    dd = data_dict.copy()
    dd.update({'include_datasets': True})
    
    data = _get_action('organization_show', context.copy(), dd)
    return data.pop('packages', [])

@p.toolkit.side_effect_free
def montrose_dataset_show_resources(context, data_dict):
    data = _get_action('package_show', context.copy(), data_dict)
    
    return data.pop('resources', [])
    
@p.toolkit.side_effect_free
def montrose_resource_show_resource_views(context, data_dict):
    data = _get_action('resource_view_list', context.copy(), data_dict)
    data = filter(lambda i: i['view_type'] == 'Chart builder', data)
    
    return data

@p.toolkit.side_effect_free
def montrose_resource_show_map_properties(context, data_dict):
    return montrose_get_geojson_properties(data_dict.get('id'))

@p.toolkit.side_effect_free
def montrose_resource_show_resource_views(context, data_dict):
    return get_resource_resource_views(data_dict.get('id'))

@p.toolkit.side_effect_free
def montrose_get_resourceview_resource_package(context, data_dict):
    return get_resourceview_resource_package(data_dict.get('resource_view_id'))

@p.toolkit.side_effect_free
def montrose_show_resource_url(context, data_dict):
    return montrose_get_resource_url(data_dict.get('id'))