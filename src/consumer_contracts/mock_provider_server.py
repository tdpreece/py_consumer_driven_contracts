import argparse


def get_commandline_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--port',
        action='store',
        help='port that mock provider is running'
    )
    return vars(parser.parse_args())


def main():
    commandline_args = get_commandline_arguments()
    host = "0.0.0.0"
    port = commandline_args.get('port')
    print('Mock provider started on {}:{}').format(host, port)
