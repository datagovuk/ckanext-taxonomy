import ckan.logic as logic

from ckanext.taxonomy.tests.test_helpers import TaxonomyTestCase

from nose.tools import raises


class TestCreateTaxonomy(TaxonomyTestCase):

    def test_create_valid(self):
        data = {
            'name': 'new-taxonomy',
            'title': 'New Taxonomy',
            'uri': 'http://localhost.local/new-taxonomy'
        }

        res = logic.get_action('taxonomy_create')(
            TestCreateTaxonomy.sysadmin_context,
            data)

        assert res['name'] == data['name'], res
        assert res['title'] == data['title'], res
        assert res['id'], res

    def test_create_valid_no_name(self):
        data = {
            'title': 'a new taxonomy',
            'uri': 'http://localhost.local/one'
        }
        res = logic.get_action('taxonomy_create')(
            TestCreateTaxonomy.sysadmin_context,
            data)

        assert res['name'] == 'a-new-taxonomy', res
        assert res['title'] == data['title'], res
        assert res['id'], res

    @raises(logic.ValidationError)
    def test_create_invalid_no_uri(self):
        data = {
            'title': 'a new taxonomy',
        }
        res = logic.get_action('taxonomy_create')(
            TestCreateTaxonomy.sysadmin_context,
            data)

    @raises(logic.ValidationError)
    def test_create_invalid(self):
        data = {}
        res = logic.get_action('taxonomy_create')(
            TestCreateTaxonomy.sysadmin_context,
            data)

    @raises(logic.ValidationError)
    def test_create_duplicate(self):
        # Attempt to create a duplicate from parent class
        data = TestCreateTaxonomy.taxonomies[0]

        res = logic.get_action('taxonomy_create')(
            TestCreateTaxonomy.sysadmin_context,
            data)

    def test_create_term_valid(self):
        data = {
            'label': 'New Term',
            'uri': 'http://localhost.local/newest-term',
            'taxonomy_id': TestCreateTaxonomy.taxonomies[0]['id'],
        }
        res = logic.get_action('taxonomy_term_create')(
            TestCreateTaxonomy.sysadmin_context,
            data)

        assert res['label'] == data['label'], res
        assert res['label'] == data['label'], res
        assert res['uri'] == data['uri'], res
        assert res['id'], res
        assert res['uri'] == data['uri'], res
        assert res['id'], res

        # cleanup
        res = logic.get_action('taxonomy_term_delete')(
            TestCreateTaxonomy.sysadmin_context,
            {'id': res['id']})

    @raises(logic.ValidationError)
    def test_create_term_invalid(self):
        # Missing URI
        data = {
            'label': 'New Term',
            'taxonomy_id': TestCreateTaxonomy.taxonomies[0]['id'],
        }
        res = logic.get_action('taxonomy_term_create')(
            TestCreateTaxonomy.sysadmin_context,
            data)

    @raises(logic.ValidationError)
    def test_create_term_invalid_label(self):
        # Missing Label
        data = {
            'uri': 'http://',
            'taxonomy_id': TestCreateTaxonomy.taxonomies[0]['id'],
        }
        res = logic.get_action('taxonomy_term_create')(
            TestCreateTaxonomy.sysadmin_context,
            data)

    def test_create_extra_valid(self):
        data = {
            'label': 'New Term',
            'uri': 'http://localhost.local/2',
            'taxonomy_id': TestCreateTaxonomy.taxonomies[0]['id'],
        }
        res = logic.get_action('taxonomy_term_create')(
            TestCreateTaxonomy.sysadmin_context,
            data)

        data = {
            'label': 'New Extra',
            'value': 'Some Extra Info',
            'term_id': res['id'],
        }
        res = logic.get_action('taxonomy_term_extra_create')(
            TestCreateTaxonomy.sysadmin_context,
            data)

        assert res['label'] == data['label'], res
        assert res['value'] == data['value'], res
        assert res['id'], res

        # cleanup
        res = logic.get_action('taxonomy_term_extra_delete')(
            TestCreateTaxonomy.sysadmin_context,
            {'id': res['id']})
