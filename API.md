
# Taxonomy API

The taxonomy API, as well as being available through the logic layer in an extension, is also available via version 3 of the CKAN API.

Calls to the CKAN API should be of the form /api/3/action/ACTION where ACTION is one of the items below.  Some of the API calls accept GET requests, in which case arguments can be provided as query parameters.

## Taxonomy object


## Taxonomy term



## taxonomy_list
**Methods**

GET, POST

**Description**

Returns a list of known taxonomies within CKAN.

**Arguments**

None

**Return value**

A list of taxonomies.


## taxonomy_show
**Methods**

GET, POST

**Description**

Shows a single taxonomy, without all of the terms it contains

**Arguments**

id - The id or short-name of the taxonomy to show, or
uri - The uri of the taxonomy to show

**Return value**

A single taxonomy


## taxonomy_create
**Methods**

POST

**Description**

Creates a new taxonomy. Terms are not created here, they must be
created using taxonomy\_term\_create with the taxonomy id from this
call provided.

**Arguments**

title - The title for the new taxonomy

name - The short-name for the new taxonomy.  If this is not specified
then it is generated from the title.  This may result in errors if the
name is already in use. It is suggested you supply the name.

uri - The URI where the taxonomy is defined.  For SKOS documents this should be the URI where the document lives.

**Return value**

The newly created taxonomy.


## taxonomy_delete
**Methods**

POST

**Description**

**Arguments**

**Return value**

The details of the taxonomy that has just been deleted.


## taxonomy_term_list
**Methods**

GET, POST

**Description**

Retrieves all of the terms for the given taxonomy

**Arguments**

id - The ID or short-name of the taxonomy from which we wish to retrieve the terms

language - The preferred language that the term labels should be shown in. If this language is not available, then it will default to the english (or main) language from the import.

**Return value**

A list of terms.


## taxonomy_term_tree
**Methods**

GET, POST

**Description**

Returns the terms for the specified taxonomy in a tree structure with each term
having a ```children``` element containing the terms that belong to that term.

**Arguments**

id - The ID or short-name of the taxonomy from which we wish to retrieve the terms

language - The preferred language that the term labels should be shown in. If this language is not available, then it will default to the english (or main) language from the import.


**Return value**

The terms for the taxonomy in a tree structure.  Be aware that a taxonomy may have more than one top-level term.


## taxonomy_term_show
**Methods**

GET, POST

**Description**


**Arguments**

**Return value**



## taxonomy_term_create
**Methods**

GET, POST

**Description**

Creates a new terms within a specific taxonomy.

**Arguments**

taxonomy_id - The name or ID of an existing taxonomy.

name - A short-name for the term

label - A default label for the term

uri - A URI describing the term (optional)

labels - A list of dictionaries where each dictionary contains a ```label``` and a ```language``` key.

**Return value**

The newly created term


## taxonomy_term_update
**Methods**

GET, POST

**Description**

**Arguments**

**Return value**



## taxonomy_term_delete
**Methods**

GET, POST

**Description**

**Arguments**

**Return value**

