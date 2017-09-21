#! /usr/bin/env python
import sys
sys.path.append('../tools/')
import csv
import pexpect
import os
import re
from env_occupation import env_occupation
from pate_conifg import search_pate_config, get_all_pates


shell_script = 'rpm_install.sh'
work_dir_on_cla = '/root'


def parse_argument():
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        if len(args) != 2:
            print_usage()
            sys.exit()
        else:
            return args
    else:
        rpm = prompt_rpm()
        host = prompt_host()
        return rpm, host


def print_usage():
    print 'usage: ' + sys.argv[0] + ' rpm host'
    print '  rpm: the name of rpm package to be install'
    print '  host: the name of target MGW'


def is_a_valid_rpm_name(name):
    if re.match('SS_MGWIWFConnMgr-trunk.*rpm', name):
        return True

    return False


def prompt_rpm():
    rpm = None
    for each in os.listdir(os.getcwd()):
        if is_a_valid_rpm_name(each):
            rpm = each
            break
    if rpm:
        answer = get_input('Give the name of rpm package you want to transfer [%s]:' % rpm)
        if len(answer) == 0:
            answer = rpm
    else:
        answer = get_input('Give the name of rpm package you want to transfer:')

    if not is_a_valid_rpm_name(answer):
        raise ValueError('Not a valid rpm')

    return answer


def prompt_host():
    all_pates = get_all_pates()
    print 'To which pate do you want to transfer:'
    for each in all_pates:
        print '  ' + each['host']
    host = get_input(':')
    if len(host) == 0:
        raise ValueError('Not a valid host name')

    return host


def get_input(words):
    return raw_input(words).strip()


def expect_password(child, psw):
    try:
        rc = child.expect(['Are you sure you want to continue connecting (yes/no)?', 'Password:'], timeout=10)
    except pexpect.TIMEOUT:
        raise Exception('Timeout when wait for prompt')
    if rc == 0:
        child.sendline('yes')
        child.expect('Password:', timeout=10)
    child.sendline(psw)


def run_command_and_expect_password(command, psw, timeout=300):
    print command
    child = pexpect.spawn(command)
    expect_password(child, psw)
    child.logfile = sys.stdout
    child.expect(pexpect.EOF, timeout=timeout)
    child.close()
    print


def ssh_run(username, psw, ip, command):
    run_command_and_expect_password("ssh %s@%s '%s'" % (username, ip, command), psw)


def transfer_file(username, psw, local, ip, remote):
    run_command_and_expect_password('scp %s %s@%s:%s' % (local, username, ip, remote), psw)


def prompt(words):
    answer = raw_input(words+'(y/n)[y]:')
    if answer.lower() == 'yes' or answer.lower() == 'y' or len(answer) == 0:
        return True

    return False


def main():
    rpm, host = parse_argument()
    record = search_pate_config(host)
    host = record['host']
    ip = record['ip']
    username = record['user']
    psw = record['password']
    print 'Install and deploy %s to %s(%s)' % (rpm, host, ip)

    try:
        env_occupation('occupy', ip, username, psw)
    except RuntimeError, e:
        print e
        exit(1)
    try:
        dirname = os.path.dirname(sys.argv[0])
        rpm_basename = os.path.basename(rpm)
        rpm_full_name_on_cla = work_dir_on_cla + '/' + rpm_basename
        ssh_run(username, psw, ip, "ls %s |grep -P ^%s$ && mv %s %s.bak"
                % (work_dir_on_cla, rpm_basename, rpm_full_name_on_cla, rpm_full_name_on_cla))
        transfer_file(username, psw, rpm, ip, work_dir_on_cla)
        transfer_file(username, psw, os.path.join(dirname, shell_script), ip, work_dir_on_cla)
        ssh_run(username, psw, ip, '/bin/bash %s %s' % (work_dir_on_cla + '/' + shell_script, rpm_full_name_on_cla))
    finally:
        env_occupation('free', ip, username, psw)


if __name__ == '__main__':
    main()
