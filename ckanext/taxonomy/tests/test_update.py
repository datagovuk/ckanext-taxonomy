import ckan.logic as logic

from ckanext.taxonomy.tests.test_helpers import TaxonomyTestCase

from nose.tools import raises

class TestUpdateTaxonomy(TaxonomyTestCase):

    def test_update_valid(self):
        tax = logic.get_action('taxonomy_show')(
            TestUpdateTaxonomy.sysadmin_context,
            {'id': TestUpdateTaxonomy.taxonomies[0]['id']})

        tax['title'] = 'Updated Title'
        updated = logic.get_action('taxonomy_update')(
            TestUpdateTaxonomy.sysadmin_context,
            tax)

        refetched = logic.get_action('taxonomy_show')(
            TestUpdateTaxonomy.sysadmin_context,
            {'id': TestUpdateTaxonomy.taxonomies[0]['id']})
        assert refetched['title'] == 'Updated Title', refetched

    @raises(logic.NotFound)
    def test_update_invalid_missing(self):
        tax = logic.get_action('taxonomy_show')(
            TestUpdateTaxonomy.sysadmin_context,
            {'id': TestUpdateTaxonomy.taxonomies[0]['id']})

        tax['id'] = 'made-up'
        updated = logic.get_action('taxonomy_term_update')(
            TestUpdateTaxonomy.sysadmin_context,
            tax)


class TestUpdateTermTaxonomy(TaxonomyTestCase):

    def setup(self):
        data = {
            'name': 'update-test',
            'label': 'New Term',
            'uri': 'http://localhost.local/update-test',
            'taxonomy_id': TestUpdateTermTaxonomy.taxonomies[0]['id'],
            'labels': [
                {'name': 'nouvelle mot', 'language': 'fr'}
            ]
        }
        res = logic.get_action('taxonomy_term_create')(
            TestUpdateTermTaxonomy.sysadmin_context,
            data)
        self.term_id = res['id']

    def teardown(self):
        res = logic.get_action('taxonomy_term_delete')(
            TestUpdateTermTaxonomy.sysadmin_context,
            {'id': self.term_id})

    def test_update_valid(self):
        term = logic.get_action('taxonomy_term_show')(
            TestUpdateTermTaxonomy.sysadmin_context,
            {'id': self.term_id})

        term['label'] = 'Updated Term'
        updated = logic.get_action('taxonomy_term_update')(
            TestUpdateTermTaxonomy.sysadmin_context,
            term)

        refetched = logic.get_action('taxonomy_term_show')(
            TestUpdateTermTaxonomy.sysadmin_context,
            {'id': self.term_id})
        assert refetched['label'] == 'Updated Term', refetched

    @raises(logic.NotFound)
    def test_update_invalid_missing(self):
        term = logic.get_action('taxonomy_term_show')(
            TestUpdateTermTaxonomy.sysadmin_context,
            {'id': self.term_id})

        term['id'] = 'made-up'
        updated = logic.get_action('taxonomy_term_update')(
            TestUpdateTermTaxonomy.sysadmin_context,
            term)
