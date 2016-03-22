import argparse
import os
import signal
import subprocess

from flask import Flask

app = Flask(__name__)


def get_commandline_arguments():
    parser = argparse.ArgumentParser()
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


@app.route('/status')
def status():
    return '{"status": "OK"}'


def main():
    commandline_args = get_commandline_arguments()
    command = commandline_args['command']
    if command == 'start':
        host = "0.0.0.0"
        port = commandline_args.get('port')
        subprocess.call([
            'gunicorn',
            '--bind',
            '0.0.0.0:1911',
            '--pid',
            '/tmp/gunicorn.pid',
            '--daemon',
            'consumer_contracts.mock_provider_server:app',
        ])
        print('Mock provider started on {}:{}').format(host, port)
    if command == 'stop':
        with open('/tmp/gunicorn.pid', 'r') as fp:
            pid = int(fp.read())
            os.kill(pid, signal.SIGTERM)
