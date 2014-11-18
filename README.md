## ckanext-taxonomy

The current support for tag vocabularies in CKAN is rather limited, and this extension provides an alternative implementation of tags, or more accurately terms where:

* Terms belong to a taxonomy which is a simple named entity
* Terms can have child terms and parent terms so that they are hierarchichal.
* Terms have a name, but also a URI, and a title which is the display string and is available in different languages.
* Terms and taxonomies can be generated from [SKOS](http://www.w3.org/2004/02/skos/specs) data.

Information about the API is available in [API.md](API.md)

## Installation

To install ckanext-taxonomy, you should follow these steps:

1. Install the code

    ```
    cd /usr/lib/ckan/default/src
    git clone https://github.com/datagovuk/ckanext-taxonomy.git
    cd ckanext-taxonomy
    python setup.py install 
    ```

2. Add ```taxonomy``` to your ckan.plugins setting in your ckan.ini file
3. Setup the database for taxonomies
4. 
    ```
    paster --plugin=ckanext-taxonomy init -c <PATH-TO-CONFIG>
    ```


## Running tests

```
cd ckanext-taxonomy
nosetests . --with-pylons=test-core.ini 
```

## Importing a SKOS document

TBC

## Removing taxonomy

If you would like to remove taxonomy you can do the following:

1. Run ```paster --plugin=ckanext-taxonomy ckeanup -c <PATH-TO-CONFIG>``` to remove the database tables
2. Remove ```taxonomy``` from your plugins section in ckan.ini