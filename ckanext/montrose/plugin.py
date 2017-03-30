import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from routes.mapper import SubMapper
from pylons import config

log = logging.getLogger(__name__)

class MontrosePlugin(plugins.SingletonPlugin):
    
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IConfigurer)

    ## IRoutes

    def before_map(self, map):

        map.redirect('/organization', '/country',
                     _redirect_code='301 Moved Permanently')

        
        map.redirect('/group', '/topic',
                     _redirect_code='301 Moved Permanently')


        
        ctrls = ['ckanext.montrose.controllers.country:CountryController', 
                 'ckanext.montrose.controllers.topic:TopicController']
        keys = ['country', 'topic']
        for ctrl, v in zip(ctrls, keys):
            with SubMapper(map, controller=ctrl) as m:
                m.connect('/delete/{}'.format(v), action='delete')
                m.connect('%s_index' % v, '/{}'.format(v), action='index')
                m.connect('/{}/list'.format(v), action='list')
                m.connect('/{}/new'.format(v), action='new')
                m.connect('{}_read'.format(v), '/%s/{id}' % v, action='read')
                m.connect('{}_edit'.format(v), '/%s/edit/{id}' % v,
                          action='edit', ckan_icon='edit')
                
                m.connect('/%s/{action}/{id}' % v,
                          requirements=dict(action='|'.join([
                              'admins',
                              'member_new',
                              'member_delete',
                              'history'
                              'followers',
                              'follow',
                              'unfollow',
                          ])))
                
                m.connect('{}_activity'.format(v), '/%s/activity/{id}' % v,
                          action='activity', ckan_icon='time')
                m.connect('{}_read'.format(v), '/%s/{id}' % v, action='read')
                m.connect('{}_about'.format(v), '/%s/about/{id}' % v,
                          action='about', ckan_icon='info-sign')
                m.connect('{}_read'.format(v), '/%s/{id}' % v, action='read',
                          ckan_icon='sitemap')
    
                m.connect('{}_members'.format(v), '/%s/members/{id}' % v,
                          action='members', ckan_icon='group')
                m.connect('{}_bulk_process'.format(v),
                          '/%s/bulk_process/{id}' % v,
                          action='bulk_process', ckan_icon='sitemap')

        return map

        
    ## IConfigurer
    
    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_resource('fanstatic', 'montrose')
        toolkit.add_public_directory(config, 'public')