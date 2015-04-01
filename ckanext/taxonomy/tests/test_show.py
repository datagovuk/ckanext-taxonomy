import ckan.logic as logic

from ckanext.taxonomy.tests.test_helpers import TaxonomyTestCase

from nose.tools import raises, assert_dict_equal


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
            'label': 'New Term',
            'uri': 'http://localhost.local',
            'taxonomy_id': TestShowTaxonomy.taxonomies[0]['id'],
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
                'label': n,
                'uri': 'http://localhost.local/%s' % n,
                'taxonomy_id': TestShowTaxonomy.taxonomies[0]['id'],
            }
            res = logic.get_action('taxonomy_term_create')(
                TestShowTaxonomy.sysadmin_context,
                data)

        bulk = logic.get_action('taxonomy_term_show_bulk')(
            TestShowTaxonomy.sysadmin_context,
            {'uris': ['http://localhost.local/%s' % n for n in names]})

        for i, n in enumerate(names):
            assert n in bulk[i]['uri'], bulk[0]
        assert len(bulk) == 2

        for n in names:
            res = logic.get_action('taxonomy_term_delete')(
                TestShowTaxonomy.sysadmin_context,
                {'uri': 'http://localhost.local/%s' % n})

    def test_term_list(self):
        total = logic.get_action('taxonomy_term_list')(
            TestShowTaxonomy.sysadmin_context,
            {'id': TestShowTaxonomy.taxonomies[0]['id']})
        old_total = len(total)

        data = {
            'label': 'New Term',
            'uri': 'http://localhost.local/1',
            'taxonomy_id': TestShowTaxonomy.taxonomies[0]['id'],
        }
        res = logic.get_action('taxonomy_term_create')(
            TestShowTaxonomy.sysadmin_context,
            data)
        assert res['id'], res

        total = logic.get_action('taxonomy_term_list')(
            TestShowTaxonomy.sysadmin_context,
            {'id': TestShowTaxonomy.taxonomies[0]['id']})
        assert len(total) == old_total + 1, len(total)

    def test_term_extra_show(self):
        data = {
            'label': 'New Term',
            'uri': 'http://localhost.local/2',
            'taxonomy_id': TestShowTaxonomy.taxonomies[0]['id'],
        }
        res = logic.get_action('taxonomy_term_create')(
            TestShowTaxonomy.sysadmin_context,
            data)
        assert res['id'], res

        term_id = res['id']

        data = {
            'label': 'New Extra',
            'value': 'Some Extra Info',
            'term_id': term_id,
        }
        new_extra = logic.get_action('taxonomy_term_extra_create')(
            TestShowTaxonomy.sysadmin_context,
            data)
        assert new_extra['id'], new_extra

        data = {
            'label': 'New Extra',
            'term_id': term_id,
        }
        saved_extra = logic.get_action('taxonomy_term_extra_show')(
            TestShowTaxonomy.sysadmin_context,
            data)
        assert saved_extra['id'], saved_extra

        assert_dict_equal(new_extra, saved_extra)

    def test_term_extra_list(self):
        data = {
            'label': 'New Term',
            'uri': 'http://localhost.local/3',
            'taxonomy_id': TestShowTaxonomy.taxonomies[0]['id'],
        }
        res = logic.get_action('taxonomy_term_create')(
            TestShowTaxonomy.sysadmin_context,
            data)
        assert res['id'], res

        total = logic.get_action('taxonomy_term_extra_list')(
            TestShowTaxonomy.sysadmin_context,
            {'id': res['id']})
        old_total = len(total)

        data = {
            'label': 'New Extra',
            'value': 'Some Extra Info',
            'term_id': res['id'],
        }
        res = logic.get_action('taxonomy_term_extra_create')(
            TestShowTaxonomy.sysadmin_context,
            data)
        assert res['id'], res

        total = logic.get_action('taxonomy_term_extra_list')(
            TestShowTaxonomy.sysadmin_context,
            {'id': res['id']})
        assert len(total) == old_total + 1, len(total)
