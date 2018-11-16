#! /usr/bin/env python
import re


def calc_result(n, k):
    if k % pow(2, n) == pow(2, n) - 1:
        return 'ON'
    return 'OFF'


def main(input_file, output_file):
    pattern = re.compile('(\d+) (\d+)')
    chain = []
    with open(input_file) as fd_in:
        for each in fd_in:
            result = pattern.match(each)
            if result:
                num_switch = int(result.groups()[0])
                num_click = int(result.groups()[1])
                chain.append((num_switch, num_click))

    lines = []
    pattern = 'Case #%d: %s\n'
    for i in range(len(chain)):
        lines.append(pattern % (i+1, calc_result(*chain[i])))

    with open(output_file, 'wb') as fd_out:
        fd_out.writelines(lines)

if __name__ == '__main__':
    main('Chain.small.1496813881326.input.txt', 'small.output')
    main('Chain.large.1496817594915.input.txt', 'large.output')


