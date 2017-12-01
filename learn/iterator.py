from unittest import TestCase, main


class IterationProtocol(object):
    def __init__(self, finish=0):
        self._cur = 0
        self._finish = finish

    def next(self):
        if self._cur < self._finish:
            return_value = self._cur
            self._cur += 1
            return return_value
        else:
            raise StopIteration('handle this')

    def __iter__(self):
        return self


class TestIterationProtocol(TestCase):
    def test_iteration_protocal(self):
        i = 0
        for each in IterationProtocol(5):
            self.assertEqual(each, i)
            i += 1


def generator_is_iterable(finish=0):
    for i in range(finish):
        yield i


class TestGeneratorIsIterable(TestCase):
    def test_generator_is_iterable(self):
        i = 0
        for each in generator_is_iterable(5):
            self.assertEqual(each, i)
            i += 1


class MyIterFunctionIsGenerator(object):
    def __init__(self, finish=0):
        self._finish = finish

    def __iter__(self):
        for each in range(self._finish):
            yield each


class TestMyIterFunctionIsGenerator(TestCase):
    def test_my_iter_function_is_generator(self):
        i = 0
        for each in MyIterFunctionIsGenerator(5):
            self.assertEqual(each, i)
            i += 1


if __name__ == '__main__':
    main(verbosity=2)
