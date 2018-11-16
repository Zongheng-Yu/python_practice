import functools
import unittest


# Not recommended, won't be supported at python3
class Comparable(object):
    def __init__(self, key):
        self._key = key

    def __cmp__(self, other):
        return self.key - other.key

    @property
    def key(self):
        return self._key


# recommended
@functools.total_ordering
class RichComparison(object):
    def __init__(self, key):
        self._key = key

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key

    @property
    def key(self):
        return self._key


class TestComparison(unittest.TestCase):
    def test_comparable(self):
        a = Comparable(1)
        b = Comparable(1)
        c = Comparable(3)
        self.assertTrue(a == b)
        self.assertTrue(a < c)

    def test_rich_comparison(self):
        a = RichComparison(1)
        b = RichComparison(1)
        c = RichComparison(3)
        self.assertTrue(a == b)
        self.assertTrue(a < c)


if __name__ == '__main__':
    unittest.main(verbosity=2)
