import re
import unittest


class TestRe(unittest.TestCase):
    def test_findall(self):
        sample = 'TCU-1         82%    17%     3%    20%     2%     2%    136      0\n' \
                 'TCU-2         82%    17%     3%    20%     2%     2%    136      0'
        pattern = re.compile('TCU-(\d+)\s+\d+%\s+(\d+)%')
        result = pattern.findall(sample)
        print result

    def test_findall2(self):
        sample = 'TCU-1\nTCU-2\nTCU-3'
        pattern = re.compile('TCU-(\d+)')
        result = pattern.findall(sample)
        print result