import ckan.logic as logic

from ckanext.taxonomy.tests.test_helpers import TaxonomyTestCase

from nose.tools import raises

class TestDeleteTaxonomy(TaxonomyTestCase):


    def help_create(self, data):
        return logic.get_action('taxonomy_create')(
            TestDeleteTaxonomy.sysadmin_context,
            data)

    def test_delete_valid(self):

        res = logic.get_action('taxonomy_list')(
            TestDeleteTaxonomy.sysadmin_context,
            {})
        total = len(res)

        # Add a taxonomy to be deleted
        data = {
            'name': 'new-taxonomy',
            'title': 'New Taxonomy',
            'uri': 'http://localhost.local/test'
        }
        res = self.help_create(data)
        data['id'] = res['id']

        assert res['name'] == data['name'], res
        assert res['title'] == data['title'], res
        assert res['id'], res

        # Create a term to make sure it is deleted
        term = logic.get_action('taxonomy_term_create')(
            TestDeleteTaxonomy.sysadmin_context,
            { 'name':'test-todelete', 'label': 'test',
              'uri': 'http://localhost.local/test-todelete', 'taxonomy_id': res['id']})

        # Delete the taxonomy
        res = logic.get_action('taxonomy_delete')(
            TestDeleteTaxonomy.sysadmin_context,
            {'id': data['name']})
        assert res['name'] == data['name'], res
        assert res['id'] == data['id'], res

        # Check it is deleted
        res = logic.get_action('taxonomy_list')(
            TestDeleteTaxonomy.sysadmin_context,
            {})
        new_total = len(res)
        assert new_total == total

    @raises(logic.NotFound)
    def test_delete_invalid(self):
        res = logic.get_action('taxonomy_delete')(
            TestDeleteTaxonomy.sysadmin_context,
            {'id': 'no-such-taxonomy'})

    def test_delete_term_valid(self):
        # Create a term to make sure it is deleted
        term1 = logic.get_action('taxonomy_term_create')(
            TestDeleteTaxonomy.sysadmin_context,
            { 'name':'test-to-delete', 'label': 'test',
              'uri': 'http://localhost.local/to-delete',
              'taxonomy_id': TestDeleteTaxonomy.taxonomies[0]['id']})

        term2 = logic.get_action('taxonomy_term_create')(
            TestDeleteTaxonomy.sysadmin_context,
            { 'name':'test2', 'label': 'test2',
              'uri': 'http://',
              'taxonomy_id': TestDeleteTaxonomy.taxonomies[0]['id'],
              'parent_id': term1['id']})

        l = logic.get_action('taxonomy_term_list')(
            TestDeleteTaxonomy.sysadmin_context,
            {'id': TestDeleteTaxonomy.taxonomies[0]['id']})
        assert len(l) == 2

        res = logic.get_action('taxonomy_term_delete')(
            TestDeleteTaxonomy.sysadmin_context,
            { 'id': term1['id'] })

        l = logic.get_action('taxonomy_term_list')(
            TestDeleteTaxonomy.sysadmin_context,
            {'id': TestDeleteTaxonomy.taxonomies[0]['id']})
        assert len(l) == 0

    @raises(logic.NotFound)
    def test_delete_term_invalid(self):
        res = logic.get_action('taxonomy_term_delete')(
            TestDeleteTaxonomy.sysadmin_context,
            { 'id': 'non-existant' })
