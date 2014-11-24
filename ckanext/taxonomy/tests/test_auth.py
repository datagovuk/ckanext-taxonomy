import ckan.logic as logic

from ckanext.taxonomy.tests.test_helpers import TaxonomyTestCase

from nose.tools import raises


class TestTaxonomyAuthSuccess(TaxonomyTestCase):

    def test_tx_create(self):
        logic.check_access(
            'taxonomy_create',
            TestTaxonomyAuthSuccess.sysadmin_context, {})

    def test_tx_delete(self):
        logic.check_access(
            'taxonomy_delete',
            TestTaxonomyAuthSuccess.sysadmin_context, {})

    def test_tx_term_create(self):
        logic.check_access(
            'taxonomy_term_create',
            TestTaxonomyAuthSuccess.sysadmin_context, {})

    def test_tx_term_update(self):
        logic.check_access(
            'taxonomy_term_update',
            TestTaxonomyAuthSuccess.sysadmin_context, {})

    def test_tx_term_delete(self):
        logic.check_access(
            'taxonomy_term_delete',
            TestTaxonomyAuthSuccess.sysadmin_context, {})


class TestTaxonomyAuthFailure(TaxonomyTestCase):

    @raises(logic.NotAuthorized)
    def test_tx_create(self):
        logic.check_access('taxonomy_create', {}, {})

    @raises(logic.NotAuthorized)
    def test_tx_delete(self):
        logic.check_access('taxonomy_delete', {}, {})

    @raises(logic.NotAuthorized)
    def test_tx_term_create(self):
        logic.check_access('taxonomy_term_create', {}, {})

    @raises(logic.NotAuthorized)
    def test_tx_term_update(self):
        logic.check_access('taxonomy_term_update', {}, {})

    @raises(logic.NotAuthorized)
    def test_tx_term_delete(self):
        logic.check_access('taxonomy_term_delete', {}, {})

    @raises(logic.NotAuthorized)
    def test_tx_create_user(self):
        logic.check_access(
            'taxonomy_create',
            TestTaxonomyAuthFailure.normal_context, {})

    @raises(logic.NotAuthorized)
    def test_tx_delete_user(self):
        logic.check_access(
            'taxonomy_delete',
            TestTaxonomyAuthFailure.normal_context, {})

    @raises(logic.NotAuthorized)
    def test_tx_term_create_user(self):
        logic.check_access(
            'taxonomy_term_create',
            TestTaxonomyAuthFailure.normal_context, {})

    @raises(logic.NotAuthorized)
    def test_tx_term_update_user(self):
        logic.check_access(
            'taxonomy_term_update',
            TestTaxonomyAuthFailure.normal_context, {})

    @raises(logic.NotAuthorized)
    def test_tx_term_delete_user(self):
        logic.check_access(
            'taxonomy_term_delete',
            TestTaxonomyAuthFailure.normal_context, {})
