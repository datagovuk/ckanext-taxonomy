
import ckan.lib.navl.dictization_functions as df
import ckan.logic as logic

Invalid = df.Invalid
StopOnError = df.StopOnError
Missing = df.Missing
missing = df.missing


def taxonomy_exists(value, context):
    try:
        logic.get_action('taxonomy_show')(context, {'uri': value})
    except logic.NotFound:
        raise Invalid('Taxonomy not found')
    except logic.ValidationError:
        raise Invalid('Taxonomy not found')
    return value


def taxonomy_exists_allow_empty(value, context):
    if not value:
        return value

    try:
        logic.get_action('taxonomy_show')(context, {'uri': value})
    except logic.NotFound:
        raise Invalid('Taxonomy not found')
    except logic.ValidationError:
        raise Invalid('Taxonomy not found')

    return value


def taxonomy_term_exists(value, context):
    try:
        logic.get_action('taxonomy_term_show')(context, {'uri': value})
    except logic.NotFound:
        raise Invalid('Term not found')
    except logic.ValidationError:
        raise Invalid('Term not found')
    return value
    pass


def taxonomy_term_exists_allow_empty(value, context):
    if not value:
        return value

    try:
        logic.get_action('taxonomy_term_show')(context, {'uri': value})
    except logic.NotFound:
        raise Invalid('Term not found')
    except logic.ValidationError:
        raise Invalid('Term not found')

    return value
