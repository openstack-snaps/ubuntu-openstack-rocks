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
    cookiecutter('rock', output_dir=output_dir, extra_context={'rock_name': args.rock_name, "packages": packages})
    return 0

if __name__ == '__main__':
    sys.exit(main()) 
