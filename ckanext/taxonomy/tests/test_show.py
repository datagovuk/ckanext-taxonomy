import ckan.logic as logic

from ckanext.taxonomy.tests.test_helpers import TaxonomyTestCase

from nose.tools import raises


class TestShowTaxonomy(TaxonomyTestCase):

    def test_show_valid_name(self):
        res = logic.get_action('taxonomy_show')(
            TestShowTaxonomy.empty_context,
            {'id': 'taxonomy-one'})

    def test_show_valid_id(self):
        res = logic.get_action('taxonomy_show')(
            TestShowTaxonomy.empty_context,
            {'id': TestShowTaxonomy.taxonomies[0]['id']})

    @raises(logic.NotFound)
    def test_show_missing_name(self):
        res = logic.get_action('taxonomy_show')(
            TestShowTaxonomy.empty_context,
            {'id': 'non-existent'})

    @raises(logic.NotFound)
    def test_show_missing_id(self):
        res = logic.get_action('taxonomy_show')(
            TestShowTaxonomy.empty_context,
            {'id': '1234'})

    def test_list(self):
        res = logic.get_action('taxonomy_list')({}, {})
        assert len(res) == 2, len(res)

    def test_show_term_valid(self):
        data = {
            'name': 'new-term',
            'label': 'New Term',
            'uri': 'http://localhost.local',
            'taxonomy_id': TestShowTaxonomy.taxonomies[0]['id'],
            'labels': [
                {'name': 'nouvelle mot', 'language': 'fr'}
            ]
        }
        res = logic.get_action('taxonomy_term_create')(
            TestShowTaxonomy.sysadmin_context,
            data)
        assert res['id'], res

        res = logic.get_action('taxonomy_term_show')(
            TestShowTaxonomy.sysadmin_context,
            {'id': res['id']})
        assert res['id'], res

        # cleanup
        res = logic.get_action('taxonomy_term_delete')(
            TestShowTaxonomy.sysadmin_context,
            {'id': res['id']})

    @raises(logic.NotFound)
    def test_show_term_missing(self):
        res = logic.get_action('taxonomy_term_show')(
            TestShowTaxonomy.sysadmin_context,
            {'id': 'non-extistent'})
        assert res['id'], res

    def test_term_bulk(self):
        names = ['bulk-one', 'bulk-two']
        for n in names:
            data = {
                'name': n,
                'label': n,
                'uri': 'http://localhost.local/%s' % n,
                'taxonomy_id': TestShowTaxonomy.taxonomies[0]['id'],
                'labels': []
            }
            res = logic.get_action('taxonomy_term_create')(
                TestShowTaxonomy.sysadmin_context,
                data)

        bulk = logic.get_action('taxonomy_term_show_bulk')(
            TestShowTaxonomy.sysadmin_context,
            {'uris': ['http://localhost.local/%s' % n for n in names]})

        assert bulk[0]['name'] in names
        assert bulk[1]['name'] in names
        assert len(bulk) == 2

        for n in names:
            res = logic.get_action('taxonomy_term_delete')(
                TestShowTaxonomy.sysadmin_context,
                {'id': n})

    def test_term_list(self):
        total = logic.get_action('taxonomy_term_list')(
            TestShowTaxonomy.sysadmin_context,
            {'id': TestShowTaxonomy.taxonomies[0]['id']})
        assert len(total) == 0, total

        data = {
            'name': 'new-term',
            'label': 'New Term',
            'uri': 'http://localhost.local',
            'taxonomy_id': TestShowTaxonomy.taxonomies[0]['id'],
            'labels': [
                {'name': 'nouvelle mot', 'language': 'fr'}
            ]
        }
        res = logic.get_action('taxonomy_term_create')(
            TestShowTaxonomy.sysadmin_context,
            data)
        assert res['id'], res

        total = logic.get_action('taxonomy_term_list')(
            TestShowTaxonomy.sysadmin_context,
            {'id': TestShowTaxonomy.taxonomies[0]['id']})
        assert len(total) == 1, len(total)
