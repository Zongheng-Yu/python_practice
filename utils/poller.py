from unittest import TestCase, main


def poller(iterable):
    while True:
        for each in iterable:
            yield each


class TestPoller(TestCase):
    def test_poller(self):
        p = poller([1, 2, 3])
        self.assertEqual(1, p.next())
        self.assertEqual(2, p.next())
        self.assertEqual(3, p.next())
        self.assertEqual(1, p.next())


if __name__ == '__main__':
    main()
