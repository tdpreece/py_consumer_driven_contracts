import argparse
import os
import signal
import subprocess


def get_commandline_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--consumer_contracts',
        action='store',
        required=False,
        help='consumer_contracts module, e.g. consumer_contracts.consumer1'
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


def start_server(pid_file, address):
    subprocess.call([
        'gunicorn',
        '--bind',
        address,
        '--pid',
        pid_file,
        '--daemon',
        'consumer_contracts.mockprovider:app',
    ])
    print('Mock provider started on {}').format(address)


def main():
    commandline_args = get_commandline_arguments()
    command = commandline_args['command']
    pid_file = '/tmp/gunicorn.pid'
    port = commandline_args['port']
    address = '0.0.0.0:{}'.format(port)
    if command == 'start':
        start_server(pid_file, address)
    if command == 'stop':
        stop_server(pid_file)
