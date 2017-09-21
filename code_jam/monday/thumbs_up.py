#! /usr/bin/env python
import sys
import re


def main(input_file, output_file):
    lines = []
    with open(input_file) as fd:
        pattern = re.compile('\d+\s(\d+)')
        for each in fd:
            result = pattern.match(each)
            if result:
                line = []
                raw_data = result.groups()[0]
                for num in raw_data:
                    line.append(int(num))
                lines.append(line)

    result_lines = []
    output_str = 'Case #%d: %d\n'
    case_num = 0
    for line in lines:
        case_num += 1
        sum = 0
        supply = 0
        for i in range(len(line)):
            if sum < i:
                supply += i - sum
                sum = i
            sum += line[i]
        result_lines.append(output_str % (case_num, supply))

    with open(output_file, 'wb') as fd:
        fd.writelines(result_lines)

if __name__ == '__main__':
    # main(sys.argv[1], sys.argv[2])
    # main('Thrump.small.1496637943246.input.txt', 'Thrump.small.1496637943246.output.txt')
    main('Thrump.large.1496638289179.input.txt', 'Thrump.large.1496638289179.output.txt')