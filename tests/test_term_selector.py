from nose.tools import *
from fuzzy_adventure.query_decomposition.nlidb.term_selectors.term_selector import TermSelector

class TestTermSelector():

    def setup(self):
        self.elements = ['1', 'a', '2']
        self.types = [int, str, unicode]
        self.answers1 = ['ans1','ans2','']
        self.answers2 = ['','ans2','']
        self.answers3 = []

    def teardown(self):
        self.elements = None
        self.types = None


    # Black box testing of apply_type
    @with_setup(setup, teardown)
    def test_apply_type_bb(self):
        applied_types = TermSelector.apply_type(self.elements, self.types)

        types = map(lambda x: type(x), applied_types)
        assert_equals(types, self.types)

    # White box testing of apply_type with index out of range
    @with_setup(setup, teardown)
    def test_apply_type_wb_index(self):
        assert_raises(IndexError, TermSelector.apply_type, self.elements, self.types[0:-1])
        assert_raises(IndexError, TermSelector.apply_type, self.elements[0:-1], self.types)


    # White box testing of apply_type with something that is not a type
    @with_setup(setup, teardown)
    @raises(TypeError)
    def test_apply_type_wb_wrong_type(self):
        self.types[-1] = 'not a type'
        TermSelector.apply_type(self.elements, self.types)


    @with_setup(setup, teardown)
    def test_filter_answers(self):
        result = TermSelector.filter_answers(self.answers1)
        assert_equals(self.answers1[0], result)

        result = TermSelector.filter_answers(self.answers2)
        assert_equals(self.answers2[1], result)

        result = TermSelector.filter_answers(self.answers3)
        assert_equals(None, result)