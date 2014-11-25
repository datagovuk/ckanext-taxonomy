import logging

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
        paster taxonomy load --url URL --name NAME --title TITLE
        paster taxonomy load --filename FILE --name NAME --title TITLE

        Where:
            URL  is the url to a SKOS document
            FILE is the local path to a SKOS document
            NAME is the short-name of the taxonomy
            TITLE is the title of the taxonomy

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
        self.parser.add_option('--title', dest='title', default=None,
                               help='Title of the taxonomy')

        super(TaxonomyCommand, self).__init__(name)

    def command(self):
        '''
        Parse command line arguments and call appropriate method.
        '''
        cmd = self.args[0]
        self._load_config()

        if cmd == 'load':
            self.load()
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

        graph = rdflib.Graph()
        result = graph.parse(url or filename)
        loader = skos.RDFLoader(graph, max_depth=1, lang='en')
        loader.flat = True

        concepts = loader.getConcepts()

        top_level = []
        for _, v in concepts.iteritems():
            if v.broader:
                top_level.append(v)

        print len(top_level)
        for t in top_level:
            print t.prefLabel.encode('utf-8')

        """

        x = concepts['http://unstats.un.org/unsd/cr/references/cofog/version1/03']
        print "altLabel", x.altLabel
        print "broader", x.broader
        print "collections", x.collections
        print "definition", x.definition
        print "metadata", x.metadata
        print "narrower", x.narrower
        print "notation", x.notation
        print "prefLabel", x.prefLabel.encode('utf-8')
        print "related", x.related
        print "schemes", x.schemes
        print "synonyms", x.synonyms
        print "uri", x.uri

        ['altLabel', 'broader', 'collections', 'definition',
        'metadata', 'narrower', 'notation', 'prefLabel',
        'related', 'schemes', 'synonyms', 'uri']
        """