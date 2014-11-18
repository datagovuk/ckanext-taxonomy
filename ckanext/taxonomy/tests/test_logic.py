import ckan.logic as logic
import pprint

from ckanext.taxonomy.tests.test_helpers import TaxonomyTestCase

from nose.tools import raises

class TestTreeLogic(TaxonomyTestCase):

    def test_gather(self):
        from ckanext.taxonomy.actions import _gather

        d = {
            "id": 1,
            "children": [
                {"id": 2, "children": []},
                {"id": 3, "children": [
                    {"id": 4}
                ]}
            ]
        }
        res = _gather(d, "id")
        assert res == [1, 2, 3, 4], res

    def test_tree(self):
        from ckanext.taxonomy.actions import _append_children
        import time

        s = time.time()
        top_terms = [
            {"id": 1, "parent_id": 0},
            {"id": 2, "parent_id": 0},
            {"id": 3, "parent_id": 0},
        ]
        all_terms = top_terms + [
            {"id": 4, "parent_id": 1},
            {"id": 5, "parent_id": 2},
            {"id": 6, "parent_id": 3},
            {"id": 7, "parent_id": 3},
            {"id": 8, "parent_id": 7},
        ]

        for t in top_terms:
            _append_children(t, all_terms)

        assert len(top_terms[0]['children']) == 1
        assert top_terms[0]['children'][0]['id'] == 4
        assert len(top_terms[1]['children']) == 1
        assert top_terms[1]['children'][0]['id'] == 5
        assert len(top_terms[2]['children']) == 2
        assert top_terms[2]['children'][0]['id'] == 6
        assert top_terms[2]['children'][1]['id'] == 7

        assert (time.time() - s) < 0.05


    def test_large_tree(self):
        """
        This test is purely testing performance of the _append_child call
        and making sure it isn't too slow
        """
        from ckanext.taxonomy.actions import _append_children
        from random import randint
        import time

        s = time.time()
        top_terms = []
        for x in range( 1, 50):
            top_terms.append({'id': x, 'parent_id': 0})

        all_terms = []
        all_terms.extend(top_terms)

        for x in range(1, 100):
            all_terms.append({'id': 50+x, 'parent_id': randint(1,50)})


        for x in range(1, 100):
            all_terms.append({'id': 150+x, 'parent_id': randint(150, 250)})

        for t in top_terms:
            _append_children(t, all_terms)

        assert (time.time() - s) < 0.02