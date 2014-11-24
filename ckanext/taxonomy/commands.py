import logging

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
        paster taxonomy load --url URL --name NAME
        paster taxonomy load --filename FILE --name NAME

        Where:
            URL  is the url to a SKOS document
            FILE is the local path to a SKOS document
            NAME is the name of the taxonomy

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
