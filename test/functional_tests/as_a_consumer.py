import mock
from StringIO import StringIO
import subprocess
from unittest import TestCase


class MockProviderSmokeTest(TestCase):
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_status_OK_returned_when_mock_up_and_running(self, stdout):
        # start mock server with port and hostname
        # send request to /status
        # Check that response is 200 and contains {'status': 'OK'}
        host = '0.0.0.0'
        port = '1911'
        subprocess.call(['mockprovider', '-h', host, '-p', port])
        expected_startup_message = 'Mock provider started on {}:{}'.format(
            host,
            port
        )
        self.assertEqual(stdout.getvalue(), expected_startup_message)
