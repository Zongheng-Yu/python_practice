import unittest


class Creature(object):
    WHO_AM_I = 'creature'

    def __init__(self):
        self.name = 'creature'

    def self_introduction(self):
        return self.name + ' is ' + self.WHO_AM_I


class Animal(Creature):
    WHO_AM_I = 'animal'

    def __init__(self):
        super(Animal, self).__init__()
        self.name = 'animal'


class Plant(Creature):
    def __init__(self):
        super(Plant, self).__init__()
        self.name = 'plant'


class Microorganism(Creature):
    WHO_AM_I = 'microorganism'

    def __init__(self):
        self.name = 'microorganism'
        pass

    def self_introduction(self):
        return super(Microorganism, self).self_introduction()


class Subcreature(Creature):
    WHO_AM_I = 'creature'

    def __init__(self):
        super(Subcreature, self).__init__()

    def self_introduction(self):
        return self.name + ' is ' + self.WHO_AM_I


class TestInheritance(unittest.TestCase):
    def test_inheritance(self):
        self.assertEqual(Animal().self_introduction(), 'animal is animal')
        self.assertEqual(Plant().self_introduction(), 'plant is creature')
        self.assertEqual(Microorganism().self_introduction(), 'microorganism is microorganism')
        self.assertEqual(Subcreature().self_introduction(), 'creature is creature')


if __name__ == '__main__':
    unittest.main()