from nose.tools import *
from fuzzy_adventure.query_decomposition import permutation

class TestPermutation():

    def setup(self):
        self.elements = ['1', 'a', '2']
        self.types = [int, str, unicode]
        self.answers1 = ['ans1','ans2','']
        self.answers2 = ['','ans2','']
        self.answers3 = []

    def teardown(self):
        self.elements = None
        self.types = None
