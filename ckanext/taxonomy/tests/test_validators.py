import ckan.logic as logic
import ckan.lib.navl.dictization_functions as df

from nose.tools import raises

from ckanext.taxonomy.tests.test_helpers import TaxonomyTestCase
from ckanext.taxonomy.validators import (taxonomy_exists,
                                         taxonomy_exists_allow_empty,
                                         taxonomy_term_exists,
                                         taxonomy_term_exists_allow_empty)


class TestValidators(TaxonomyTestCase):

    def test_taxonomy_exists_ok(self):
        val = taxonomy_exists(
            "http://localhost.local/taxonomy-one",
            TestValidators.normal_context
        )
        assert val == "http://localhost.local/taxonomy-one"

    @raises(df.Invalid)
    def test_taxonomy_missing(self):
        val = taxonomy_exists(
            "http://localhost.local/made-up-uri",
            TestValidators.normal_context
        )

    @raises(df.Invalid)
    def test_taxonomy_no_value(self):
        val = taxonomy_exists(
            "",
            TestValidators.normal_context
        )

    def test_taxonomy_no_value_ok(self):
        val = taxonomy_exists_allow_empty(
            "",
            TestValidators.normal_context
        )
        assert val == "", val

    @raises(df.Invalid)
    def test_taxonomy_no_value_wrong_val(self):
        val = taxonomy_exists_allow_empty(
            "non-existent",
            TestValidators.normal_context
        )

    def test_taxonomy_term_exists_ok(self):
        data = {
            'name': 'new-term-test',
            'label': 'New Term',
            'uri': 'http://localhost.local/newest-term',
            'taxonomy_id': TestValidators.taxonomies[0]['id'],
            'labels': [
                {'name': 'nouvelle mot', 'language': 'fr'}
            ]
        }
        res = logic.get_action('taxonomy_term_create')(
            TestValidators.sysadmin_context,
            data)

        val = taxonomy_term_exists(
            "http://localhost.local/newest-term",
            TestValidators.normal_context
        )
        assert val == "http://localhost.local/newest-term"

    @raises(df.Invalid)
    def test_taxonomy_term_missing(self):
        val = taxonomy_term_exists(
            "http://localhost.local/made-up-uri",
            TestValidators.normal_context
        )

    @raises(df.Invalid)
    def test_taxonomy_term_no_value(self):
        val = taxonomy_term_exists(
            "",
            TestValidators.normal_context
        )

    def test_taxonomy_term_no_value_ok(self):
        val = taxonomy_term_exists_allow_empty(
            "",
            TestValidators.normal_context
        )
        assert val == "", val

    @raises(df.Invalid)
    def test_taxonomy_term_no_value_wrong_val(self):
        val = taxonomy_term_exists_allow_empty(
            "non-existent",
            TestValidators.normal_context
        )
