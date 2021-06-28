import csv
import sys
import re
import json


def parse_arg():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        raise ValueError('Please provide the input filename')


def parse_input_file(filename):
    with open(filename, newline='', encoding='utf-8') as fd:
        fd.readline()
        reader = csv.reader(fd)
        for row in reader:
            aggregate_record(*row)


output = {"records": [], "total": 0}


class Record(object):
    def __init__(self, id, testCase_id, build_id, team_id):
        self.id = id
        self.testCase_id = testCase_id
        self.build_id = build_id
        self.team_id = None
        self.execution_time = None
        self.result = None
        self.phase_id = None


result = dict()


def aggregate_record(id, testCase_id, build_id, team_id, execution_time, result, phase_id):
    re
class Result(object):
    def __init__(self):
        self.build

class Build(object):
    def __init__(self):
        self.build = None
        self.phase = None
        self.team_num = None
        self.case_num = None
        self.team_id = None
        self.pass_num = None
        self.fail_num = None
        self.case_num = None
        self.pass_rate = None

    def aggregate_record(self, id, testCase_id, build_id, team_id, execution_time, result, phase_id):


def main():
    #filename = parse_arg()
    parse_input_file(r"sample/result_case_1_1build_1phase_1team_2case_50percent_pass.csv")
    json.dump(output, sys.stdout, indent=2)


if __name__ == '__main__':
    main()
