#! /usr/bin/env python
import sys
import csv
import pexpect
import os


pate_config_file = 'pate_config.csv'
shell_script = 'rpm_install.sh'


def search_pate_config(host):
    with open(os.path.join(os.path.dirname(sys.argv[0]), pate_config_file)) as fd:
        data = csv.reader(fd)
        for each in data:
            if each[0] == host:
                return each
        else:
            raise Exception('Host name(%s) not found in pate config file.' % host)


def parse_argument():
    args = sys.argv[1:]
    if len(args) != 2:
        print_usage()
        sys.exit()
    else:
        return args


def print_usage():
    print 'usage: ' + sys.argv[0] + ' rpm host'
    print '  rpm: the name of rpm package to be install'
    print '  host: the name of target MGW'


def expect_password(child, psw):
    try:
        rc = child.expect(['Are you sure you want to continue connecting (yes/no)?', 'Password:'], timeout=10)
    except pexpect.TIMEOUT:
        raise Exception('Timeout in connecting to ' + ip)
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
    os.getcwd()
    rpm, host = parse_argument()
    host, ip, username, psw = search_pate_config(host)
    if not prompt('Are you sure you want to install and deploy %s to %s(%s)?' % (rpm, host, ip)):
        exit()
    dirname = os.path.dirname(sys.argv[0])
    transfer_file(username, psw, rpm, ip, '/tmp')
    transfer_file(username, psw, os.path.join(dirname, shell_script), ip, '/tmp')
    ssh_run(username, psw, ip, '/bin/bash /tmp/%s /tmp/%s' % (shell_script, os.path.basename(rpm)))


if __name__ == '__main__':
    main()

