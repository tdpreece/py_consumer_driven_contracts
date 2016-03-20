import argparse
import os

import daemon
from flask import Flask

app = Flask(__name__)


def get_commandline_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--port',
        action='store',
        help='port that mock provider is running'
    )
    return vars(parser.parse_args())


@app.route('/status')
def status():
    return '{"status": "OK"}'


def main():
    commandline_args = get_commandline_arguments()
    host = "0.0.0.0"
    port = commandline_args.get('port')
    pid = os.fork()
    if pid == 0:
        with daemon.DaemonContext():
            app.run(host, port)
    else:
        print('Mock provider started on {}:{}').format(host, port)
