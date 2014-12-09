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

----

**WARNING**: Importing will currently delete an existing taxonomy if it exists with the same name.  If you are using term uris in your schema this shouldn't be a problem if you are copying the same taxonomy over the top.

----

Import DGU themes (rdf in repo)

```
paster taxonomy load --filename dgu-themes.rdf --name dgu --title "DGU Themes" \
    --uri "http://data.gov.uk/themes"
```

Importing cofog from a file ...

```
paster taxonomy load --filename COFOG.rdf --name cofog  \
    --title cofog --uri "http://unstats.un.org/unsd/cr/registry/regcst.asp?Cl=4"
```

Importing eurovoc from a file ... **warning** this is slow.

```
paster taxonomy load --filename eurovoc_skos.rdf --name eurovoc  \
    --title "EuroVOC" --uri "http://eurovoc.europa.eu/schema"
```


Importing from a url ...

```
paster taxonomy load --url http://..../COFOG.rdf --name cofog  \
    --title cofog --uri "http://unstats.un.org/unsd/cr/registry/regcst.asp?Cl=4"
    ```

## Taxonomies

CoFoG - http://unstats.un.org/unsd/cr/registry/regcst.asp?Cl=4

Eurovoc - http://publications.europa.eu/mdr/resource/thesaurus/eurovoc/skos/eurovoc_skos.zip


## Removing taxonomy

If you would like to remove taxonomy you can do the following:

1. Run ```paster --plugin=ckanext-taxonomy cleanup -c <PATH-TO-CONFIG>``` to remove the database tables
2. Remove ```taxonomy``` from your plugins section in ckan.ini