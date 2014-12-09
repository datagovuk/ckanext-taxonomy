import ckan.logic as logic
import ckan.lib.navl.dictization_functions as df

from nose.tools import raises

from ckanext.taxonomy.tests.test_helpers import TaxonomyTestCase
from ckanext.taxonomy.converters import (taxonomy_to_dict,
                                         taxonomy_terms_to_dicts)

class TestConverters(TaxonomyTestCase):

    def setup(self):
        self.terms = []
        data = [{
            'name': 'converter-test-1',
            'label': 'Converter Test 1',
            'uri': 'http://localhost.local/converter-1',
            'taxonomy_id': TestConverters.taxonomies[0]['id'],
        },{
            'name': 'converter-test-2',
            'label': 'Converter Test 2',
            'uri': 'http://localhost.local/converter-2',
            'taxonomy_id': TestConverters.taxonomies[0]['id'],
        }]
        for d in data:
            res = logic.get_action('taxonomy_term_create')(
                TestConverters.sysadmin_context,
                d)
            self.terms.append(res['id'])

    def teardown(self):
        for t in self.terms:
            res = logic.get_action('taxonomy_term_delete')(
                TestConverters.sysadmin_context,
                {'id': t})

    def test_taxonomy_to_dict(self):
        tx = TestConverters.taxonomies[0]
        res = taxonomy_to_dict(tx['uri'], TestConverters.normal_context)
        assert res['uri'] == tx['uri'], res

    def test_taxonomy_to_dict_fail(self):
        tx = TestConverters.taxonomies[0]
        res = taxonomy_to_dict("not-found", TestConverters.normal_context)
        assert res is None, res

    def test_taxonomy_terms_to_dicts(self):
        res = taxonomy_terms_to_dicts(
            '["http://localhost.local/converter-2",\
              "http://localhost.local/converter-1"]',
            TestConverters.normal_context)
        assert len(res) == 2, res
        assert res[0]['uri'] == 'http://localhost.local/converter-1'
        assert res[1]['uri'] == 'http://localhost.local/converter-2'

    def test_taxonomy_terms_to_dicts_single(self):
        res = taxonomy_terms_to_dicts(
            '["http://localhost.local/converter-2"]',
            TestConverters.normal_context)
        assert len(res) == 1, res
        assert res[0]['uri'] == 'http://localhost.local/converter-2'

    def test_taxonomy_terms_to_dicts_fails_not_found(self):
        res = taxonomy_terms_to_dicts(
            '["http://localhost.local/converter-22"]',
            TestConverters.normal_context)
        assert len(res) == 0, res

    def test_taxonomy_terms_to_dicts_fails_not_found(self):
        res = taxonomy_terms_to_dicts(
            '[]',
            TestConverters.normal_context)
        assert res is None, res

    def test_taxonomy_terms_single_to_dicts_fails(self):
        res = taxonomy_terms_to_dicts(
            '',
            TestConverters.normal_context)
        assert res is None, res

    def test_taxonomy_terms_single_bad_json(self):
        res = taxonomy_terms_to_dicts(
            "'not really json",
            TestConverters.normal_context)
        assert res is None, res
