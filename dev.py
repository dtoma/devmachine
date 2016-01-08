#!/usr/bin/env python3


import argparse
import os
import requests
import subprocess


parser = argparse.ArgumentParser(description='Create a development environment.',
                                 prog='dev')

parser.add_argument('os',
                    type=str,
                    help='OS/version to use')

parser.add_argument('packages',
                    type=str,
                    nargs='+',
                    help='list of packages to install')

vagrantfile_url = 'https://raw.githubusercontent.com/dtoma/vagrantfiles/master/{}/Vagrantfile'

roles_url = 'https://raw.githubusercontent.com/dtoma/ansible-playbooks/master/roles/{}/tasks/main.yml'


def parse_cmdline():
    """Parse the command-line arguments to get the OS and the list of packages to install."""
    args = parser.parse_args()
    vm_os = args.os
    print('OS:', vm_os)
    vm_packages = args.packages + ['update']
    print('Packages:', ', '.join(vm_packages))
    return vm_os, vm_packages


def download_vagrantfile(vm_os):
    """Download the Vagrantfile from GitHub."""
    print('Download Vagrantfile')
    resp = requests.get(vagrantfile_url.format(vm_os))
    if resp.status_code == 200:
        with open('Vagrantfile', 'w+') as vf:
            vf.write(resp.text)
        print('Done')


def download_ansible_roles(vm_packages):
    """Download the ansible roles from GitHub."""
    # Simple for now, rework later to handle templates
    for role in vm_packages:
        print('Download ansible role for {}'.format(role))
        resp = requests.get(roles_url.format(role))
        if resp.status_code == 200:
            os.makedirs('./roles/{}/tasks'.format(role), exist_ok=True)
            with open('./roles/{}/tasks/main.yml'.format(role), 'w+') as yml:
                yml.write(resp.text)
        print('Done')


def write_playbook(roles):
    """Write a playbook that calls a list of roles."""
    print('Write ansible playbook')
    with open('playbook.yml', 'w+') as pb:
        pb.write(('---\n'
                  '- hosts: all\n'
                  '  sudo: yes\n'
                  '  tasks:\n'))
        pb.write('    - include: roles/update/tasks/main.yml\n')
        for role in roles:
            pb.write('    - include: roles/{}/tasks/main.yml\n'.format(role))
    print('Done')


def create_workspace():
    """Create a folder to share with the VM."""
    print('Create workspace')
    os.makedirs('./workspace', exist_ok=True)
    print('Done')


def run_vagrant_up():
    """Run vagrant up to create and provision the VM."""
    subprocess.call('vagrant up', shell=True)


if __name__ == '__main__':
    vm_os, vm_packages = parse_cmdline()

    download_vagrantfile(vm_os)

    download_ansible_roles(vm_packages)

    write_playbook(vm_packages)

    create_workspace()

    run_vagrant_up()
