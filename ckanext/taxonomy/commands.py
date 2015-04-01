import logging
import json

import rdflib
import skos

import ckan.lib.cli as cli

log = logging.getLogger(__name__)


class TaxonomyCommand(cli.CkanCommand):
    '''  A command for working with taxonomies

    Usage::

     # Initialising the database
     paster taxonomy init

     # Remove the database tables
     paster taxonomy cleanup

     # Loading a taxonomy
     paster taxonomy load --url URL --name NAME --title TITLE --lang LANG --uri URI
     paster taxonomy load --filename FILE --name NAME --title TITLE --lang LANG --uri URI

     Where:
       URL  is the url to a SKOS document
       FILE is the local path to a SKOS document
       NAME is the short-name of the taxonomy
       TITLE is the title of the taxonomy
       LANG (optional) is a language identifier, e.g. en, es, fr
       URI is a uri for the taxonomy

    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__

    def __init__(self, name):
        self.parser.add_option('--filename', dest='filename', default=None,
                               help='Path to a file')
        self.parser.add_option('--url', dest='url', default=None,
                               help='URL to a resource')
        self.parser.add_option('--name', dest='name', default=None,
                               help='Name of the taxonomy to work with')
        self.parser.add_option('--title', dest='title', default='',
                               help='Title of the taxonomy')
        self.parser.add_option('--lang', dest='lang', default='en',
                               help='Language to use when retrieving labels')
        self.parser.add_option('--uri', dest='uri', default='',
                               help='The URI of the taxonomy')

        super(TaxonomyCommand, self).__init__(name)

    def command(self):
        '''
        Parse command line arguments and call appropriate method.
        '''
        cmd = self.args[0]
        self._load_config()

        if cmd == 'load':
            self.load()
        elif cmd == 'load-extras':
            self.load_extras()
        elif cmd == 'init':
            self.init()
        elif cmd == 'cleanup':
            self.cleanup()
        else:
            print self.usage
            log.error('Command "%s" not recognized' % (cmd,))
            return

    def init(self):
        from ckanext.taxonomy.models import init_tables
        init_tables()

    def cleanup(self):
        from ckanext.taxonomy.models import remove_tables
        remove_tables()

    def load(self):
        url = self.options.url
        filename = self.options.filename
        if not url and not filename:
            print "No URL or FILENAME provided and one is required"
            print self.usage
            return

        if not self.options.name:
            print "No NAME provided and it is required"
            print self.usage
            return

        if not self.options.uri:
            print "No URI provided and it is required"
            print self.usage
            return

        print "Loading graph"
        graph = rdflib.Graph()
        result = graph.parse(url or filename)
        loader = skos.RDFLoader(graph,
                                max_depth=float('inf'),
                                flat=True,
                                lang=self.options.lang)

        print "Processing concepts"
        concepts = loader.getConcepts()

        top_level = []
        for _, v in concepts.iteritems():
            if not v.broader:
                top_level.append(v)
        top_level.sort(key=lambda x: x.prefLabel)

        import ckan.model as model
        import ckan.logic as logic

        self.context = {'model': model, 'ignore_auth': True }

        try:
            current = logic.get_action('taxonomy_show')(
                self.context,
                {'id': self.options.name})
            logic.get_action('taxonomy_delete')(
                self.context,
                {'id': self.options.name})
        except logic.NotFound:
            pass

        tx = logic.get_action('taxonomy_create')(self.context, {
            'title': self.options.title or self.options.name,
            'name': self.options.name,
            'uri': self.options.uri
        })

        for t in top_level:
            self._add_node(tx, t)

    def load_extras(self):
        filename = self.options.filename
        if not filename:
            print "No FILENAME provided and it is required"
            print self.usage

        name = self.options.name
        if not name:
            print "No NAME provided and it is required"
            print self.usage
            return

        with open(filename) as input_file:
            extras = json.loads(input_file.read())

        import ckan.model as model
        import ckan.logic as logic

        self.context = {'model': model, 'ignore_auth': True }

        taxonomy_terms = logic.get_action('taxonomy_term_list')(self.context, {'name': name})
        taxonomy_lookup = dict([(term['label'], term) for term in taxonomy_terms])

        for term in extras:
            term_name = term['title']
            term_id = taxonomy_lookup[term_name]['id']

            for extra in term.keys():
                if extra in ['title', 'stored_as', 'description']:
                    continue

                data = {
                    'term_id': term_id,
                    'label': extra,
                }
                existing_extra = logic.get_action('taxonomy_term_extra_show')(self.context, data)

                data = {
                    'label': extra,
                    'value': json.dumps(term[extra]),
                    'term_id': term_id,
                }
                if existing_extra:
                    data['id'] = existing_extra['id']
                    logic.get_action('taxonomy_term_extra_update')(self.context, data)
                else:
                    logic.get_action('taxonomy_term_extra_create')(self.context, data)


    def _add_node(self, tx, node, parent=None, depth=1):
        import ckan.model as model
        import ckan.logic as logic
        import ckan.lib.munge as munge

        print '   ' * depth, node.prefLabel.encode('utf-8')

        description = ''
        if hasattr(node, 'definition') and node.definition:
            description = node.definition.encode('utf-8')

        print type(node)
        # rdfs:comment print dir(node)

        nd = logic.get_action('taxonomy_term_create')(self.context,  {
            'label': node.prefLabel.encode('utf-8'),
            'uri': node.uri,
            'description': description,
            'taxonomy_id': tx['id'],
            'parent_id': parent
        })
        node_id = nd['id']


        for _, child in node.narrower.iteritems():
            self._add_node(tx, child, node_id, depth+1)
