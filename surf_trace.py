#! /usr/bin/env python
import getopt
import sys
import os
import re


trace_flag = None
iwf_blade_index = 0
trace_path = '/tmp/surf_trace'


def usage():
    print 'usage:'
    print ' -t, --trace             Value should be on or off'
    print ' -i, --iwf_blade_index   The index of IWF blade should be between 0 and 3. 0 is the default value.'
    print ' -p, --get_trace_path    Print the trace file storage path'
    print ' -h, --help              Print this usage '


def parse_argv():
    global trace_flag
    global iwf_blade_index
    opts = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], 't:i:ph',
                                   ['trace=', 'iwf_blade_index=', 'get_trace_path', 'help'])
    except getopt.GetoptError:
        usage()
        exit(1)

    for option, value in opts:
        if option in ['-h', '--help']:
            usage()
            exit()
        elif option in ['-p', '--get_trace_path']:
            print trace_path
            exit()
        elif option in ['-t', '--trace']:
            if value not in ['on', 'off']:
                usage()
                exit(1)
            else:
                trace_flag = value
        elif option in ['-i', '--iwf_blade_index']:
            # each MGW shelf have Max of 4 iwf blades
            if value not in ['0', '1', '2', '3']:
                usage()
                exit(1)
            else:
                iwf_blade_index = int(value)

    if not trace_flag:
        usage()
        exit(1)


def del_trace_dir():
    run_cmd = 'ssh iwf-' + str(iwf_blade_index) + ' rm -rf ' + trace_path
    if os.system(run_cmd) != 0:
        print 'Error: failed when trying to run following command: '
        print run_cmd
        exit(1)


def get_iwfmu_physical_addr(iwf_index):
    command = ''' ilclifunit -v|grep -i '/IWF-%s/MGW_IWFMFU'|awk '{print $6" "$3}' ''' % iwf_index
    output = os.popen(command)
    pattern = re.compile('MGW_IWFMFU')
    for line in output:
        if pattern.search(line):
            rg_name, addr = line.split()
            addr = int(addr, 16)
            break
    else:
        raise Exception('failed to get physical addr')
    return addr


def trace_process():
    if trace_flag == 'on':
        on_or_off = 1
        # delete surf trace folder since no one delete it when last case run done
        del_trace_dir()
    else:
        on_or_off = 0

    addr = get_iwfmu_physical_addr(iwf_blade_index)
    command = "ilcliru.sh /CLA-0/MGW_CMFU-0 dmxsend -- -a 7002,c385,0,0 -h *,%04x,0b4c,0,0,0,0,3a64,0003 -b xb1,xb%d"\
              % (addr, on_or_off)
    print command
    if os.system(command) != 0:
        print 'Error: failed setting trace ' + trace_flag
        exit(1)


if __name__ == '__main__':
    parse_argv()
    trace_process()
