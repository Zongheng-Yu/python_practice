#!/usr/bin/env python
import re

if __name__ == '__main__':
    with open('command_list', 'w') as ofs:
        with open('software_list') as fs:
            pattern = re.compile('(.*)\s+\((.*)\)')
            for each in fs:
                result = pattern.match(each)
                if result:
                    command = 'pip install %s==%s\n' % result.groups()
                    ofs.writelines(command)
                else:
                    raise Exception("not match regular: " + each)
