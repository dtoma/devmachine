#!/usr/bin/env python3

"""Create dev VM using vagrant and ansible."""


import argparse
import os
import subprocess

import requests


PARSER = argparse.ArgumentParser(description='Create a development environment.',
                                 prog='dev')

PARSER.add_argument('os',
                    type=str,
                    help='OS/version to use')

PARSER.add_argument('packages',
                    type=str,
                    nargs='*',
                    help='list of packages to install')

RAW_GITHUB_URL = 'https://raw.githubusercontent.com/dtoma/'

VAGRANTFILE_URL = RAW_GITHUB_URL + 'vagrantfiles/master/{}/Vagrantfile'

ROLES_URL = RAW_GITHUB_URL + 'ansible-playbooks/master/roles/{}/tasks/main.yml'


def parse_cmdline():
    """Parse the command-line arguments to get the OS and the list of packages to install."""
    args = PARSER.parse_args()
    return args.os, args.packages + ['update']


def download_vagrantfile(distro):
    """Download the Vagrantfile from GitHub."""
    print('Download Vagrantfile')

    resp = requests.get(VAGRANTFILE_URL.format(distro))

    if resp.status_code == 200:
        with open('Vagrantfile', 'w') as vfile:
            vfile.write(resp.text)

        print('Done')


def download_ansible_roles(roles):
    """Download the ansible roles from GitHub."""

    # Simple for now, rework later to handle templates
    for role in roles:
        print('Download ansible role for {}'.format(role))
        resp = requests.get(ROLES_URL.format(role))

        if resp.status_code == 200:
            os.makedirs('./roles/{}/tasks'.format(role), exist_ok=True)

            with open('./roles/{}/tasks/main.yml'.format(role), 'w+') as yml:
                yml.write(resp.text)

        print('Done')


def write_playbook(roles):
    """Write a playbook that calls a list of roles."""
    print('Write ansible playbook')

    with open('playbook.yml', 'w') as pbook:
        pbook.write(('---\n'
                     '- hosts: all\n'
                     '  sudo: yes\n'
                     '  tasks:\n'))
        pbook.write('    - include: roles/update/tasks/main.yml\n')

        for role in roles:
            pbook.write('    - include: roles/{}/tasks/main.yml\n'.format(role))

    print('Done')


def create_workspace():
    """Create a folder to share with the VM."""
    print('Create workspace')
    os.makedirs('./workspace', exist_ok=True)
    print('Done')


def run_vagrant_up():
    """Run vagrant up to create and provision the VM."""
    subprocess.call('vagrant up', shell=True)


def main():
    """Script entry point."""
    vm_os, vm_packages = parse_cmdline()
    print('OS:', vm_os)
    print('Packages:', ', '.join(vm_packages))

    download_vagrantfile(vm_os)

    download_ansible_roles(vm_packages)

    write_playbook(vm_packages)

    create_workspace()

    run_vagrant_up()


if __name__ == '__main__':
    main()
