import ckan.lib.base as base
import ckan.logic as logic
import ckan.model as model
import ckan.plugins as p
import ckan.plugins.toolkit as toolkit

class TaxonomyController(base.BaseController):

    def index(self):
        context = {
            'model': model,
            'user': toolkit.c.user
        }

        toolkit.c.taxonomies = logic.get_action('taxonomy_list')(context, {})

        return toolkit.render('ckanext/taxonomy/index.html')

    def show(self, name):
        context = {
            'model': model,
            'user': toolkit.c.user
        }

        toolkit.c.taxonomy = logic.get_action('taxonomy_show')(
            context,
            {'id': name})

        toolkit.c.terms = logic.get_action('taxonomy_term_tree')(
            context,
            {'id': toolkit.c.taxonomy['id']})

        return toolkit.render('ckanext/taxonomy/show.html')
