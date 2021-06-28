#!/usr/bin/env python3
import sys
import yaml
import subprocess
import re


def get_vlan_interface_name(interface_name, is_oam):
    if is_oam:
        mapping = {'fm_a': 'fronthaul_a', 'fm_b': 'fronthaul_b'}
    else:
        mapping = {'fm_a': 'f1om_a',
                   'fm_b': 'f1om_b',
                   'fh_a': 'fronthaul_a',
                   'fh_b': 'fronthaul_b',
                   'bh_a': 'backhaul_a',
                   'bh_b': 'backhaul_b'}
    return mapping[interface_name]


def log(msg):
    print(msg)


def load_rcp_config():
    with open('metadate.yaml') as fp:
        return yaml.load(fp.read())


def check_platform(cfg):
    """
    only run on VCP1.0 platform
    """
    if 'cloudplatform' in cfg and (cfg['cloudplatform'].upper() == 'VCP1' or cfg['cloudplatform'].upper() == 'OSP'):
        log("start to run script to config VLAN and external ips")
    else:
        log("no need to start up this script  cause it is not VCP1.0")
        sys.exit()


def get_hostname():
    with open('/etc/hostname') as fd:
        hostname = fd.readline().strip()
    return hostname


def create_vlan_interface(hostname, name, eth, sid):
    cmd = 'vlanipcli -v -o %s -n %s -r %s -d %s' % (hostname, name, eth, sid)
    log(cmd)
    subprocess.run(cmd.split())


def create_ip(hostname, interface, cidr, ip_type, roles=None):
    ip, mask = cidr.split('/')
    cmd = 'vlanipcli -p -o {} -i {} -a {} -m {} -t {}'.format(hostname, interface, ip, mask, ip_type)
    if roles:
        for each in roles:
            cmd += ' -l ' + each.strip()
    log(cmd)
    subprocess.run(cmd.split())


def is_loop_back(eth):
    if eth[-3:] == '_lo':
        return True
    return False


def config_vlan_and_external_ip(ip_sid_info, is_2n=False):
    hostname = get_hostname()
    is_oam = False
    pattern = 'oam-\d+$'
    if re.search(pattern, hostname, re.IGNORECASE):
        is_oam = True
    for eth, value in ip_sid_info.items():
        addresses = []
        if isinstance(value['ip_addrs'], list):
            addresses = value['ip_addrs']
        elif isinstance(value['ip_addrs'], str):
            addresses = [value['ip_addrs']]
        ip_type = 'PHYSICAL'
        if is_2n and eth[:3] != 'fm_':
            ip_type = 'LOGICAL'
        if is_2n and is_oam and eth[:3] == 'fm_':
            ip_type = 'LOGICAL'
        if is_loop_back(eth):
            for cidr in addresses:
                try:
                    create_ip(hostname, 'lo', cidr, ip_type, get_role_list(value['role']))
                except Exception as e:
                    print(e)
        else:
            vif_name = get_vlan_interface_name(eth, is_oam)
            create_vlan_interface(hostname, vif_name, eth, value['sid'])
            for cidr in addresses:
                create_ip(hostname, vif_name, cidr, ip_type)


def get_role_list(roles):
    role_list = []
    if isinstance(roles, list):
        role_list = roles
    elif isinstance(roles, str) and roles.strip():
        role_list = roles.strip().split(',')
    return role_list


def get_ip_list(ip_addrs):
    addresses = []
    if isinstance(ip_addrs, list):
        addresses = ip_addrs
    elif isinstance(ip_addrs, str):
        addresses = [ip_addrs]
    return addresses


def create_service_vlan(hostname, name, sid, master_eth, backup_eth):
    # todo
    cmd = 'vlanipcli -v -o %s -n %s -r %s -x %s -d %s' % (hostname, name, master_eth, backup_eth, sid)
    log(cmd)
    subprocess.run(cmd.split())


def config_sid_and_external_ip(lrip_app_info, master_eth, backup_eth, is_2n):
    # todo
    hostname = get_hostname()
    for vif_name, value in lrip_app_info.items():
        create_service_vlan(hostname, vif_name, value['sid'], master_eth, backup_eth)
        for each in value['ip_role_list']:
            addresses = get_ip_list(each['ip_addrs'])
            roles = get_role_list(each['roles'])
            ip_type = 'PHYSICAL'
            if is_2n and ('Tracing' not in roles) and ('tracing' not in roles):
                ip_type = 'LOGICAL'
            for cidr in addresses:
                try:
                    create_ip(hostname, vif_name, cidr, ip_type, roles)
                except Exception as e:
                    print(e)


def main():
    cfg = load_rcp_config()
    check_platform(cfg)
    subprocess.run(['sudo', 'chmod', '755', '/opt/nokia/bin/vlanipcli'])
    is_2n = False
    if 'ha-mode' in cfg and cfg['ha-mode'] == '2n':
        is_2n = True
    if 'ip-sid-info' in cfg:
        config_vlan_and_external_ip(cfg['ip-sid-info'], is_2n)
    if 'lrip-app-info' in cfg:
        try:
            config_sid_and_external_ip(cfg['lrip-app-info'], cfg['lrip-info']['master-ether'],
                                       cfg['lrip-info']['backup-ether'], is_2n)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
