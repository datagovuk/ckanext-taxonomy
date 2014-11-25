import ckan.lib.base as base
import ckan.logic as logic
import ckan.model as model
import ckan.plugins as p
import ckan.plugins.toolkit as toolkit

class TaxonomyController(base.BaseController):

    def index(self):
        context = {
            'model': model,
            'user': base.c.user
        }

        base.c.taxonomies = logic.get_action('taxonomy_list')(context, {})

        return toolkit.render('ckanext/taxonomy/index.html')

    def show(self, name):
        context = {
            'model': model,
            'user': base.c.user
        }

        base.c.taxonomy = logic.get_action('taxonomy_show')(
            context,
            {'id': name})

        base.c.terms = logic.get_action('taxonomy_term_tree')(
            context,
            {'id': c.taxonomy['id']})

        return toolkit.render('ckanext/taxonomy/show.html')
