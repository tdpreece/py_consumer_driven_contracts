from __future__ import print_function, unicode_literals
import argparse
import os
import signal
import subprocess


def get_commandline_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--contracts_path',
        action='store',
        required=False,
        help='Path of consumer contracts file.'
    )
    parser.add_argument(
        '-p', '--port',
        action='store',
        required=False,
        help='port that mock provider is running'
    )
    parser.add_argument('command', nargs=1)
    arg_dict = vars(parser.parse_args())
    arg_dict['command'] = arg_dict['command'][0]
    return arg_dict


def stop_server(pid_file):
    with open(pid_file, 'r') as fp:
        pid = int(fp.read())
        os.kill(pid, signal.SIGTERM)


def start_server(pid_file, address, contracts_path):
    app = 'consumer_contracts.mockprovider:create_app("{}")'.format(
        contracts_path
    )
    subprocess.call([
        'gunicorn',
        '--bind',
        address,
        '--pid',
        pid_file,
        '--daemon',
        app,
    ])
    print(('Mock provider started on {}').format(address))


def main():
    commandline_args = get_commandline_arguments()
    command = commandline_args['command']
    pid_file = '/tmp/gunicorn.pid'
    port = commandline_args['port']
    address = '0.0.0.0:{}'.format(port)
    if command == 'start':
        contracts_path = commandline_args['contracts_path']
        start_server(pid_file, address, contracts_path)
    if command == 'stop':
        stop_server(pid_file)
