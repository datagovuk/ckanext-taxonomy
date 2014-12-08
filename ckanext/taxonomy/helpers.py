import ckan.model as model
import ckan.logic as logic


def taxonomy(named_taxonomy):
    """ Returns the named taxonomy """
    ctx = {'model': model}
    return logic.get_action('taxonomy_show')\
        (ctx, {'name': named_taxonomy})

def taxonomy_terms(taxonomy_id):
    ctx = {'model': model}
    return logic.get_action('taxonomy_term_tree')\
        (ctx, {'id': taxonomy_id})
