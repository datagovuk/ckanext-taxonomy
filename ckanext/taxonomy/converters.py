import json

import ckan.logic as logic

def taxonomy_to_dict(value, context):
    """
    Converts a term ID into the dict representation of that term
    """
    if not value:
        return None

    try:
        res = logic.get_action('taxonomy_show')(context, {'uri': value})
    except logic.NotFound:
        return None

    return res


def taxonomy_terms_to_dicts(value, context):
    """
    Converts the taxonomy term uris into a list of dictionaries
    containing the dict representation of the terms.
    """
    if not value:
        return None

    try:
        obj = json.loads(value)
        if isinstance(obj, list):
            retval = logic.get_action('taxonomy_term_show_bulk')(
                context,
                {'uris': obj})
        else:
            retval = [logic.get_action('taxonomy_term_show')(context, {'uri': value})]
    except logic.ValidationError:
        return None
    except ValueError:
        return None

    return retval
