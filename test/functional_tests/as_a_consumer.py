import subprocess
from unittest import TestCase


class MockProviderSmokeTest(TestCase):
    def test_status_OK_returned_when_mock_up_and_running(self):
        # start mock server with port and hostname
        # send request to /status
        # Check that response is 200 and contains {'status': 'OK'}
        host = '0.0.0.0'
        port = '1911'
        stdout = subprocess.check_output(
            ['mockprovider', '-h', host, '-p', port]
        )
        expected_startup_message = 'Mock provider started on {}:{}'.format(
            host,
            port
        )
        self.assertEqual(stdout.strip(), expected_startup_message)
