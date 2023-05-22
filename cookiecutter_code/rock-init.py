#!/usr/bin/env python3

import shutil
import yaml
import argparse
import tempfile
import os
import glob
from cookiecutter.main import cookiecutter
import subprocess
from pathlib import Path

from datetime import datetime
import sys

KOLLA_USERS = {
    'kolla-user': {
        'uid': 42400,
        'gid': 42400,
    },
    'ansible-user': {
        'uid': 42401,
        'gid': 42401,
    },
    'aodh-user': {
        'uid': 42402,
        'gid': 42402,
    },
    'barbican-user': {
        'uid': 42403,
        'gid': 42403,
    },
    'bifrost-user': {
        'uid': 42404,
        'gid': 42404,
    },
    'ceilometer-user': {
        'uid': 42405,
        'gid': 42405,
    },
    'cinder-user': {
        'uid': 42407,
        'gid': 42407,
    },
    'cloudkitty-user': {
        'uid': 42408,
        'gid': 42408,
    },
    'collectd-user': {
        'uid': 42409,
        'gid': 42409,
    },
    'congress-user': {  # unused user (congress dropped)
        'uid': 42410,
        'gid': 42410,
    },
    'designate-user': {
        'uid': 42411,
        'gid': 42411,
    },
    'elasticsearch-user': {  # unused user (elasticsearch dropped)
        'uid': 42412,
        'gid': 42412,
    },
    'etcd-user': {
        'uid': 42413,
        'gid': 42413,
    },
    'freezer-user': {
        'uid': 42414,
        'gid': 42414,
    },
    'glance-user': {
        'uid': 42415,
        'gid': 42415,
    },
    'gnocchi-user': {
        'uid': 42416,
        'gid': 42416,
    },
    'grafana-user': {
        'uid': 42417,
        'gid': 42417,
    },
    'heat-user': {
        'uid': 42418,
        'gid': 42418,
    },
    'horizon-user': {
        'uid': 42420,
        'gid': 42420,
    },
    'influxdb-user': {
        'uid': 42421,
        'gid': 42421,
    },
    'ironic-user': {
        'uid': 42422,
        'gid': 42422,
    },
    'kafka-user': {  # unused user (kafka dropped)
        'uid': 42423,
        'gid': 42423,
    },
    'keystone-user': {
        'uid': 42425,
        'gid': 42425,
    },
    'kibana-user': {  # unused user (kibana dropped)
        'uid': 42426,
        'gid': 42426,
    },
    'qemu-user': {
        'uid': 42427,
        'gid': 42427,
    },
    'magnum-user': {
        'uid': 42428,
        'gid': 42428,
    },
    'manila-user': {
        'uid': 42429,
        'gid': 42429,
    },
    'mistral-user': {
        'uid': 42430,
        'gid': 42430,
    },
    'monasca-user': {  # unused user (monasca dropped)
        'uid': 42431,
        'gid': 42431,
    },
    'mongodb-user': {  # unused user (mongodb dropped)
        'uid': 42432,
        'gid': 42432,
    },
    'murano-user': {
        'uid': 42433,
        'gid': 42433,
    },
    'mysql-user': {
        'uid': 42434,
        'gid': 42434,
    },
    'neutron-user': {
        'uid': 42435,
        'gid': 42435,
    },
    'nova-user': {
        'uid': 42436,
        'gid': 42436,
    },
    'octavia-user': {
        'uid': 42437,
        'gid': 42437,
    },
    'rabbitmq-user': {
        'uid': 42439,
        'gid': 42439,
    },
    'rally-user': {  # unused user (rally dropped)
        'uid': 42440,
        'gid': 42440,
    },
    'sahara-user': {
        'uid': 42441,
        'gid': 42441,
    },
    'senlin-user': {
        'uid': 42443,
        'gid': 42443,
    },
    'solum-user': {
        'uid': 42444,
        'gid': 42444,
    },
    'swift-user': {
        'uid': 42445,
        'gid': 42445,
    },
    'tacker-user': {
        'uid': 42446,
        'gid': 42446,
    },
    'td-agent-user': {
        'uid': 42447,
        'gid': 42447,
    },
    'telegraf-user': {
        'uid': 42448,
        'gid': 42448,
    },
    'trove-user': {
        'uid': 42449,
        'gid': 42449,
    },
    'vmtp-user': {  # unused user (vmtp dropped)
        'uid': 42450,
        'gid': 42450,
    },
    'watcher-user': {
        'uid': 42451,
        'gid': 42451,
    },
    'zookeeper-user': {  # unused user (zookeeper dropped)
        'uid': 42453,
        'gid': 42453,
    },
    'haproxy-user': {
        'uid': 42454,
        'gid': 42454,
    },
    'memcached-user': {
        'uid': 42457,
        'gid': 42457,
    },
    'vitrage-user': {
        'uid': 42459,
        'gid': 42459,
    },
    'redis-user': {
        'uid': 42460,
        'gid': 42460,
    },
    'ironic-inspector-user': {
        'uid': 42461,
        'gid': 42461,
    },
    'odl-user': {
        'uid': 42462,
        'gid': 42462,
    },
    'zun-user': {
        'uid': 42463,
        'gid': 42463,
    },
    'dragonflow-user': {  # unused user (dragonflow dropped)
        'uid': 42464,
        'gid': 42464,
    },
    'qdrouterd-user': {   # unused user (qdrouterd dropped)
        'uid': 42465,
        'gid': 42465,
    },
    'ec2api-user': {
        'uid': 42466,
        'gid': 42466,
    },
    'sensu-user': {  # unused used (sensu dropped)
        'uid': 42467,
        'gid': 42467,
    },
    'skydive-user': {  # unused user (skydive dropped)
        'uid': 42468,
        'gid': 42468,
    },
    'kuryr-user': {
        'uid': 42469,
        'gid': 42469,
    },
    'blazar-user': {
        'uid': 42471,
        'gid': 42471,
    },
    'prometheus-user': {
        'uid': 42472,
        'gid': 42472,
    },
    'libvirt-user': {
        'uid': 42473,  # unused user, but we need the group for socket access
        'gid': 42473,
    },
    'fluentd-user': {
        'uid': 42474,
        'gid': 42474,
    },
    'almanach-user': {  # unused user (almanach dropped)
        'uid': 42475,
        'gid': 42475,
    },
    'openvswitch-user': {
        'uid': 42476,  # unused user
        'gid': 42476,
    },
    'hugetlbfs-user': {
        'uid': 42477,  # unused user, but we need the group for vhost socket
        'gid': 42477,
    },
    'logstash-user': {  # unused user (elasticsearch dropped)
        'uid': 42478,
        'gid': 42478,
    },
    'storm-user': {
        'uid': 42479,
        'gid': 42479,
    },
    'tempest-user': {  # unused user (tempest dropped)
        'uid': 42480,
        'gid': 42480,
    },
    'nfast-user': {
        'uid': 42481,  # unused user, but we need the group for thales hsm
        'gid': 42481,
    },
    'placement-user': {
        'uid': 42482,
        'gid': 42482,
    },
    'cyborg-user': {
        'uid': 42483,
        'gid': 42483,
    },
    'masakari-user': {
        'uid': 42485,
        'gid': 42485,
    },
    'hacluster-user': {
        'uid': 42486,
        'gid': 42486,
        'group': 'haclient',
    },
    'proxysql-user': {
        'uid': 42487,
        'gid': 42487,
    },
    'letsencrypt-user': {
        'uid': 42488,
        'gid': 42488,
    },
    'venus-user': {
        'uid': 42489,
        'gid': 42489,
    },
    'opensearch-user': {
        'uid': 42490,
        'gid': 42490,
    },
    'skyline-user': {
        'uid': 42491,
        'gid': 42491,
    }
}

def get_suggested_packages(container_name):
    container_packages = {
        'cinder-api': "cinder-api  apache2 libapache2-mod-wsgi-py3 openssl",
        'cinder-scheduler': "cinder-scheduler",
        'cinder-volume': "lsscsi multipath-tools nfs-common nvme-cli sysfsutils targetcli-fb thin-provisioning-tools tgt cinder-volume python3-rtslib-fb",
        'glance-api': "nfs-common qemu-utils  glance python3-boto3 python3-os-brick python3-oslo.vmware python3-rados python3-rbd apache2 libapache2-mod-wsgi-py3 openssl",
        'openstack-dashboard': "openstack-dashboard apache2 libapache2-mod-wsgi-py3 openssl",
        'keystone': "libapache2-mod-auth-gssapi python3-requests-kerberos keystone libapache2-mod-auth-mellon libapache2-mod-auth-openidc python3-ldappool",
        'neutron-server': "python3-ironic-neutron-agent python3-neutron-dynamic-routing python3-neutron-vpnaas iproute2 iputils-ping keepalived net-tools radvd neutron-plugin-ml2 neutron-server openvswitch-switch python3-networking-sfc python3-openvswitch python3-oslo.vmware",
        'nova-api': "nova-api python3-memcache nova-common openvswitch-switch python3-nova ovmf apache2 libapache2-mod-wsgi-py3 openssl patch",
        'nova-conductor': "nova-conductor nova-common openvswitch-switch python3-nova ovmf",
        'nova-scheduler': "nova-schedule nova-common openvswitch-switch python3-nova ovmf",
        'ovn-sb-db-server': "ovn-central ovn-common openvswitch-switch python3-openvswitch python3-netifaces tcpdump",
        'ovn-nb-db-server': "ovn-central ovn-common openvswitch-switch python3-openvswitch python3-netifaces tcpdump",
        'ovn-northd': "ovn-central ovn-common openvswitch-switch python3-openvswitch python3-netifaces tcpdump",
        'placement-api': "placement-api placement-common python3-memcache apache2 libapache2-mod-wsgi-py3 openssl"
    }
    return container_packages.get(container_name)

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('rock_name', help='Name of rock')
    return parser.parse_args()


def main() -> int:
    """Echo the input arguments to standard output"""
    args = arg_parser()
    cookie_dir = Path(__file__).resolve().parent
    output_dir = cookie_dir  / "../rocks/"
    output_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(cookie_dir)
    packages = "sudo " + get_suggested_packages(args.rock_name)
    username = args.rock_name.split('-')[0]
    print(f"{username}-user")
    cookiecutter(
        'rock',
        output_dir=output_dir,
        extra_context={
            'rock_name': args.rock_name,
            "username": username,
            "packages": packages,
            'uid': KOLLA_USERS.get(f"{username}-user", {}).get('uid')})
    return 0

if __name__ == '__main__':
    sys.exit(main()) 
