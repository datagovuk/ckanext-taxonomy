import ckan.model as model

from ckan.tests import BaseCase
from ckan.lib.create_test_data import CreateTestData

from ckanext.taxonomy.models import Taxonomy, init_tables, remove_tables


class TaxonomyTestCase(BaseCase):

    @classmethod
    def setup_class(cls):
        model.repo.init_db()
        init_tables()
        cls.setup_users()
        cls.setup_taxonomy_data()

    @classmethod
    def setup_users(cls):
        CreateTestData.create_users([{
            u'name': u'sysadmin',
            u'fullname': u'Test Sysadmin',
            u'password': u'pass',
            u'sysadmin': True
        }, {
            u'name': u'test',
            u'fullname': u'Test user',
            u'password': u'pass',
            u'sysadmin': False
        }])
        cls.sysadmin_context = {'user': 'sysadmin', 'model': model}
        cls.normal_context = {'user': 'test', 'model': model}
        cls.empty_context = {'user': '', 'model': model}

    @classmethod
    def setup_taxonomy_data(cls):
        if model.Session.query(Taxonomy).count() > 0:
            return

        cls.taxonomies = [{
            u'name': u'taxonomy-one',
            u'title': u'Taxonomy One',
            u'uri': u'http://localhost.local/taxonomy-one'
        }, {
            u'name': u'taxonomy-two',
            u'title': u'Taxonomy Two',
            u'uri': u'http://localhost.local/taxonomy-two'
        }]
        for t in cls.taxonomies:
            tx = Taxonomy(**t)
            model.Session.add(tx)
            model.Session.commit()
            t['id'] = tx.id

    @classmethod
    def teardown_class(cls):
        model.repo.rebuild_db()
        remove_tables()
        model.Session.remove()
