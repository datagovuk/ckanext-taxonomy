"""
    :type groups: list of dictionaries
    :param owner_org: the id of the dataset's owning organization, see

   :returns: the newly created dataset (unless 'return_id_only' is set to True
              in the context, in which case just the dataset id will
              be returned)
    :rtype: dictionary
"""

import json

import ckan.plugins.toolkit as toolkit
import ckan.logic as logic

from ckan.lib.munge import munge_name
from ckanext.taxonomy.models import Taxonomy, TaxonomyTerm

_check_access = logic.check_access


@toolkit.side_effect_free
def taxonomy_list(context, data_dict):
    """ List all of the known taxonomies

    :returns: A list of taxonomies currently installed
    :rtype: A list of dictionaries.
    """
    _check_access('taxonomy_list', context, data_dict)

    model = context['model']
    items = model.Session.query(Taxonomy).order_by('title')
    return [item.as_dict() for item in items.all()]


@toolkit.side_effect_free
def taxonomy_show(context, data_dict):
    """ Shows a single taxonomy.

    The id (or name) of the taxonomy is required as an id
    parameter in the data_dict. Alternatively taxonomies can
    be found using their uri field.

    :returns: A single taxonomy
    :rtype: A dictionary
    """
    _check_access('taxonomy_show', context, data_dict)

    model = context['model']
    id = data_dict.get('id')
    uri = data_dict.get('uri')
    name = data_dict.get('name')

    if not id and not uri and not name:
        raise logic.ValidationError("Neither id, name or uri were provided")

    item = Taxonomy.get(id or name)
    if not item and uri:
        item = Taxonomy.by_uri(uri)

    if not item:
        raise logic.NotFound()

    return item.as_dict(with_terms=True)


def taxonomy_create(context, data_dict):
    """
    Creates a new taxonomy. Terms are not created here, they must be
    created using taxonomy_term_create with the taxonomy id from this
    call.

    title is required, name will be generated from title if no name is
    provided but if this clashes it will generate an error (i.e. better
    to set the name yourself).

    :returns: The newly created taxonomy
    :rtype: A dictionaries.
    """
    _check_access('taxonomy_create', context, data_dict)

    model = context['model']

    name = data_dict.get('name')
    title = logic.get_or_bust(data_dict, 'title')
    uri = logic.get_or_bust(data_dict, 'uri')

    if not name:
        name = munge_name(title)

    # Check the name has not been used
    if model.Session.query(Taxonomy).filter(Taxonomy.name == name).count() > 0:
        raise logic.ValidationError("Name is already in use")

    t = Taxonomy(name=name, title=title, uri=uri)
    model.Session.add(t)
    model.Session.commit()

    return t.as_dict()


def taxonomy_update(context, data_dict):
    """
    Updates an existing taxonomy.

    title, name and uri are required

    :returns: The newly updated taxonomy
    :rtype: A dictionary
    """
    _check_access('taxonomy_update', context, data_dict)

    model = context['model']

    id = logic.get_or_bust(data_dict, 'id')
    name = logic.get_or_bust(data_dict, 'name')
    title = logic.get_or_bust(data_dict, 'title')
    uri = logic.get_or_bust(data_dict, 'uri')

    tax = Taxonomy.get(id)
    if not tax:
        raise logic.NotFound()

    tax.name = name
    tax.title = title
    tax.uri = uri

    model.Session.add(tax)
    model.Session.commit()

    return tax.as_dict()


def taxonomy_delete(context, data_dict):
    """
    Delete the specific taxonomy, and as a result, all of the terms within
    it.

    :returns: The newly deleted taxonomy
    :rtype: A dictionary
    """
    _check_access('taxonomy_delete', context, data_dict)

    model = context['model']

    name = logic.get_or_bust(data_dict, 'id')

    taxonomy = Taxonomy.get(name)
    if not taxonomy:
        raise logic.NotFound()

    terms = model.Session.query(TaxonomyTerm)\
        .filter(TaxonomyTerm.taxonomy == taxonomy)
    map(model.Session.delete, terms.all())

    model.Session.delete(taxonomy)
    model.Session.commit()

    return taxonomy.as_dict()


@toolkit.side_effect_free
def taxonomy_term_list(context, data_dict):
    """
    Lists all of the taxonomy terms for the given taxonomy.

    If 'language' is specified in data_dict (default is en) then
    it will return the label for that language.

    :returns: The list of terms for the specified taxonomy
    :rtype: A list of term dictionaries
    """
    _check_access('taxonomy_term_list', context, data_dict)

    model = context['model']
    top_only = context.get('top_only', False)

    language = data_dict.get('language', 'en')

    context['with_terms'] = False
    taxonomy = logic.get_action('taxonomy_show')(context, data_dict)
    terms = model.Session.query(TaxonomyTerm)\
        .filter(TaxonomyTerm.taxonomy_id == taxonomy['id'])

    if top_only:
        terms = terms.filter(TaxonomyTerm.parent.is_(None))
    terms = terms.order_by(TaxonomyTerm.label).all()

    return [term.as_dict(language) for term in terms]


@toolkit.side_effect_free
def taxonomy_term_tree(context, data_dict):
    """
    Returns the taxonomy terms as a tree for the given taxonomy

    If 'language' is specified in data_dict (default is en) then
    it will return the label for that language.

    :returns: The taxonomy's terms as a tree structure
    :rtype: A list of dictionaries.
    """
    _check_access('taxonomy_term_tree', context, data_dict)

    model = context['model']

    context['with_terms'] = False
    taxonomy = logic.get_action('taxonomy_show')(context, data_dict)

    all_terms = logic.get_action('taxonomy_term_list')(context, data_dict)
    top_terms = [t for t in all_terms if t['parent_id'] is None]

    # We definitely don't want each term to be responsible for loading
    # it's children.  Maybe we should do that here per top_term using the
    # results from top_list. Need to measure but I think up to 100 or so items
    # this may well be faster than lots of DB trips.  May need optimising.
    terms = [_append_children(term, all_terms) for term in top_terms]

    return terms


@toolkit.side_effect_free
def taxonomy_term_show(context, data_dict):
    """
    Shows a single taxonomy term and its children, the taxonomy id is not
    required, just a term_id.

    :returns: A single taxonomy term
    :rtype: A dictionary
    """
    _check_access('taxonomy_term_show', context, data_dict)
    model = context['model']

    id = data_dict.get('id')
    uri = data_dict.get('uri')

    if not id and not uri:
        raise logic.ValidationError("Either id or uri is required")

    if id:
        term = TaxonomyTerm.get(id)
    elif uri:
        term = TaxonomyTerm.by_uri(uri)

    if not term:
        raise logic.NotFound()

    return term.as_dict()


@toolkit.side_effect_free
def taxonomy_term_show_bulk(context, data_dict):
    """
    When given a list of URIs this function will return a list
    of taxonomy terms.

    :returns: All of the terms found from the supplied uris
    :rtype: A list of dictionaries
    """
    _check_access('taxonomy_term_show', context, data_dict)
    model = context['model']

    uris = data_dict.get('uris')
    if not uris:
        raise logic.ValidationError("A list of URIs is required")

    term_items = model.Session.query(TaxonomyTerm).\
        filter(TaxonomyTerm.uri.in_(uris))
    return [t.as_dict() for t in term_items]


def taxonomy_term_create(context, data_dict):
    """ Allows for the creation of a mew taxonomy term.

    :returns: The newly updated term
    :rtype: A dictionary
    """
    _check_access('taxonomy_term_create', context, data_dict)
    model = context['model']

    taxonomy_id = logic.get_or_bust(data_dict, 'taxonomy_id')
    taxonomy = logic.get_action('taxonomy_show')(context, {'id': taxonomy_id})

    # ensure name is in the data_dict
    name = logic.get_or_bust(data_dict, 'name')
    label = logic.get_or_bust(data_dict, 'label')
    uri = logic.get_or_bust(data_dict, 'uri')

    # Check the name has not been used
    if model.Session.query(TaxonomyTerm).\
            filter(TaxonomyTerm.name == name).count() > 0:
        raise logic.ValidationError("Name is already in use")
    if model.Session.query(TaxonomyTerm).\
            filter(TaxonomyTerm.uri == uri).count() > 0:
        raise logic.ValidationError("URI is already in use")

    labels = data_dict.pop('labels', [])
    term = TaxonomyTerm(**data_dict)
    term.set_labels(labels)

    model.Session.add(term)
    model.Session.commit()

    return term.as_dict()


def taxonomy_term_update(context, data_dict):
    """ Allows a taxonomy term to be updated.

    :returns: The newly updated term
    :rtype: A dictionary
    """
    _check_access('taxonomy_term_update', context, data_dict)
    model = context['model']

    id = logic.get_or_bust(data_dict, 'id')

    term = TaxonomyTerm.get(id)
    if not term:
        raise logic.NotFound()

    term.name = data_dict.get('name', term.name)
    term.label = data_dict.get('label', term.label)
    term.parent_id = data_dict.get('parent_id', term.parent_id)
    term.uri = logic.get_or_bust(data_dict, 'uri')
    term.set_labels(data_dict.get('labels', []))

    model.Session.add(term)
    model.Session.commit()

    return term.as_dict()


def taxonomy_term_delete(context, data_dict):
    """ Deletes a taxonomy term.

    This call deletes all of its child terms (those in narrower scope).

    :returns: The newly deleted term
    :rtype: A dictionary
    """
    _check_access('taxonomy_term_delete', context, data_dict)
    model = context['model']

    term = logic.get_action('taxonomy_term_show')(context, data_dict)

    all_terms = logic.get_action('taxonomy_term_list')(
        context, {'id': term['taxonomy_id']})
    _append_children(term, all_terms)

    # Now we just need to iterate through the tree and gather up IDs
    # to delete....
    ids = _gather(term, 'id')
    todelete = model.Session.query(TaxonomyTerm).\
        filter(TaxonomyTerm.id.in_(ids))

    if len(ids):
        map(model.Session.delete, todelete)
        model.Session.commit()

    return term


def _gather(d, key):
    """
    Gather the values in d making sure we navigate down all 'children' nodes
    """
    res = []
    for k, v in d.iteritems():
        if k == key:
            res.append([v])
        if k == 'children':
            for c in v:
                res.append(_gather(c, key))

    # Flatten the list before returning it.
    return reduce(lambda h, t: h+t, res)


def _append_children(term, terms):
    term['children'] = [t for t in terms if t['parent_id'] == term['id']]

    for t in term['children']:
        _append_children(t, terms)

    return term
