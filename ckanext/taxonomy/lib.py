import json

import ckan.model as model
import ckan.logic as logic
from ckan.plugins import toolkit as tk


def load_term_extras(filepath, taxonomy_name):
    '''
    Load extra information about the terms already in a taxonomy

    These are loaded from a JSON file which contains an Array of Objects
    which have a 'title' key which corresponds to the 'label' of the
    taxonomy term.

    [{"title": "term1",
      "extra1", "value2",
      "extra2", "value2",
      ...
      },
      ...
     ]

    This file format has been adopted from the themes.json file used in
    data.gov.uk. As well as the 'title', key which is used to match up with
    the 'label' of the taxonomy term, the keys 'description' and
    'stored_as' are also removed from the object before storing it in the
    JSON extras field.
    '''
    with open(filepath) as input_file:
        extras_list = json.loads(input_file.read())

        context = {'model': model, 'ignore_auth': True}

        data = {'name': taxonomy_name}
        taxonomy_terms = logic.get_action('taxonomy_term_list')(context, data)
        taxonomy_term_lookup = dict([(term['label'], term)
                                     for term in taxonomy_terms])

        for extras in extras_list:
            term_name = extras['title']
            for key in ['title', 'description', 'stored_as']:
                if key in extras:
                    # Remove the unwanted keys from themes.json
                    del extras[key]

            term = taxonomy_term_lookup[term_name]
            term['extras'] = extras
            logic.get_action('taxonomy_term_update')(context, term)


def load_terms_and_extras(filepath, taxonomy_name, taxonomy_title=None):
    '''
    Load terms and extras from file as a taxonomy. This can be used by tests
    needing to load a bunch of terms from a JSON file.

    These are loaded from a JSON file which contains an Array of Objects
    which have a 'title' key which corresponds to the 'label' of the
    taxonomy term.

    [{"title": "term1",
      "description": "This is a term",
      "extra1", "value2",
      "extra2", "value2",
      ...
      },
      ...
     ]

    This file format has been adopted from the themes.json file used in
    data.gov.uk.
    '''
    context = {'model': model, 'ignore_auth': True}
    try:
        taxonomy = tk.get_action('taxonomy_show')(context,
                                                  {'id': taxonomy_name})
    except tk.ObjectNotFound:
        taxonomy = tk.get_action('taxonomy_create')(context,
                                                    {'title': taxonomy_title,
                                                     'name': taxonomy_name,
                                                     'uri': ''})
    with open(filepath) as input_file:
        term_list = json.loads(input_file.read())

    existing_terms = logic.get_action('taxonomy_term_list')(context, {'name': taxonomy_name})
    existing_term_lookup = dict([(term['label'], term)
                                 for term in existing_terms])

    for term_from_file in term_list:
        term_name = term_from_file['title']
        extras = dict(((k, v) for k, v in term_from_file.items()
                       if k not in ('title', 'description', 'stored_as')))
        term = dict(taxonomy_id=taxonomy['id'],
                    label=term_name,
                    description=term_from_file.get('description', ''),
                    uri='http://data.gov.uk/data/theme/%s' % (term_from_file.get('stored_as') or term_name),
                    stored_as=term_from_file.get('stored_as', ''),
                    extras=extras)
        if term_name in existing_term_lookup:
            term['id'] = existing_term_lookup[term_name]['id']
            logic.get_action('taxonomy_term_update')(context, term)
        else:
            logic.get_action('taxonomy_term_create')(context, term)
        existing_terms = logic.get_action('taxonomy_term_list')(context, {'name': taxonomy_name})
