import subprocess
from unittest import TestCase

import requests


class MockProviderSmokeTest(TestCase):
    def test_status_OK_returned_when_mock_up_and_running(self):
        host = '0.0.0.0'
        port = '1911'
        # start server
        stdout = subprocess.check_output(
            ['mockprovider', '-p', port, 'start']
        )
        expected_startup_message = 'Mock provider started on {}:{}'.format(
            host,
            port
        )
        self.assertEqual(stdout.strip(), expected_startup_message)

        # Check server is running
        status_url = 'http://{}:{}/status'.format(host, port)
        response = requests.get(status_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), {"status": "OK"})

        # stop server
        stdout = subprocess.check_output(
            ['mockprovider', '-p', port, 'stop']
        )
        with self.assertRaises(requests.ConnectionError):
            response = requests.get(status_url)
