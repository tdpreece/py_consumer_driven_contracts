import mock
from unittest import TestCase

from consumer_contracts.mock_provider_server import get_commandline_arguments


class TestGetCommandLineArguments(TestCase):
    def test_port_returned_when_present(self):
        port = 'aport'
        with mock.patch('sys.argv', ['', '-p', port]):
            args = get_commandline_arguments()
            self.assertIn('port', args)
            self.assertEqual(args['port'], port)
