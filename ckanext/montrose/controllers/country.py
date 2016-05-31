import re

import ckan.controllers.group as group
import ckan.plugins as plugins


class CountryController(group.GroupController):

    group_types = ['organization']

    def _guess_group_type(self, expecting_name=False):
        return 'organization'

    def _replace_group_org(self, string):
        ''' substitute organization for group if this is an org'''
        return re.sub('^group', 'organization', string)

    def _update_facet_titles(self, facets, group_type):
        for plugin in plugins.PluginImplementations(plugins.IFacets):
            facets = plugin.organization_facets(
                facets, group_type, None)
