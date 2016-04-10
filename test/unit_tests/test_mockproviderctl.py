import mock
from unittest import TestCase

from consumer_contracts.mockproviderctl import get_commandline_arguments


class TestGetCommandLineArguments(TestCase):
    def test_port_returned_when_present(self):
        port = 'aport'
        command = 'start'
        command_line_args = ['', '-p', port, '-c', 'contracts', command]
        with mock.patch('sys.argv', command_line_args):
            args = get_commandline_arguments()
            self.assertIn('port', args)
            self.assertEqual(args['port'], port)

    def test_command_returned(self):
        port = 'aport'
        command = 'start'
        command_line_args = ['', '-p', port, '-c', 'contracts', command]
        with mock.patch('sys.argv', command_line_args):
            args = get_commandline_arguments()
            self.assertIn('command', args)
            self.assertEqual(args['command'], command)
