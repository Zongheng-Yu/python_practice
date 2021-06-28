import re
import csv


def main(input_file, output_file):
    pattern = re.compile('^<\?xml version=')
    xmls= list()
    xml = None
    input_lines = []
    with open(input_file) as input_fd:
        input_lines = input_fd.readlines()

    for line in input_lines:
        if re.search(pattern, line):
            if xml is not None:
                xmls.append(xml)
            xml = list()
        if xml is not None:
            xml.append(line)

    for xml in xmls:
        print('.................................................')
        for line in xml:
            print(line)


if __name__ == '__main__':
    main("RESULTS_TA_POLQA.txt", "RESULTS_TA_POLQA.csv")
