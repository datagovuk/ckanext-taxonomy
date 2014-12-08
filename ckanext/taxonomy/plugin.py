from logging import getLogger

import ckan.plugins as p

log = getLogger(__name__)


class TaxonomyPlugin(p.SingletonPlugin):
    '''
    Taxonomy plugin that provides hierarchical 'tags'.
    '''

    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IActions, inherit=True)
    p.implements(p.IAuthFunctions, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)

    def before_map(self, map):
        ctrl = 'ckanext.taxonomy.controllers:TaxonomyController'
        map.connect('taxonomies_index', '/taxonomies',
            controller=ctrl,
            action='index')
        map.connect('taxonomies_show', '/taxonomies/:name',
            controller=ctrl,
            action='show')
        return map

    def after_map(self, map):
        return map

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_public_directory(config, 'public')

    def get_helpers(self):
        """
        A dictionary of extra helpers that will be available to provide
        taxonomy helpers to the templates.
        """
        from ckanext.taxonomy import helpers
        from inspect import getmembers, isfunction

        helper_dict = {}

        functions_list = [o for o in getmembers(helpers, isfunction)]
        for name, fn in functions_list:
            if name[0] != '_':
                helper_dict[name] = fn

        return helper_dict

    def get_actions(self):
        import ckanext.taxonomy.actions as actions
        return {
            'taxonomy_list':        actions.taxonomy_list,
            'taxonomy_show':        actions.taxonomy_show,
            'taxonomy_create':      actions.taxonomy_create,
            'taxonomy_delete':      actions.taxonomy_delete,
            'taxonomy_update':      actions.taxonomy_update,

            'taxonomy_term_list':   actions.taxonomy_term_list,
            'taxonomy_term_tree':   actions.taxonomy_term_tree,
            'taxonomy_term_show':   actions.taxonomy_term_show,
            'taxonomy_term_show_bulk': actions.taxonomy_term_show_bulk,
            'taxonomy_term_create': actions.taxonomy_term_create,
            'taxonomy_term_update': actions.taxonomy_term_update,
            'taxonomy_term_delete': actions.taxonomy_term_delete
        }

    def get_auth_functions(self):
        import ckanext.taxonomy.auth as auth
        return {
            'taxonomy_list':        auth.taxonomy_list,
            'taxonomy_show':        auth.taxonomy_show,
            'taxonomy_create':      auth.taxonomy_create,
            'taxonomy_delete':      auth.taxonomy_delete,
            'taxonomy_update':      auth.taxonomy_update,

            'taxonomy_term_list':   auth.taxonomy_term_list,
            'taxonomy_term_tree':   auth.taxonomy_term_tree,
            'taxonomy_term_show':   auth.taxonomy_term_show,
            'taxonomy_term_create': auth.taxonomy_term_create,
            'taxonomy_term_update': auth.taxonomy_term_update,
            'taxonomy_term_delete': auth.taxonomy_term_delete
        }
