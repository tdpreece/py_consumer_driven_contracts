import subprocess
from time import sleep
from unittest import TestCase

import requests


class TestControlOfMockProviderServer(TestCase):
    def test_server_starts_up_and_stops(self):
        host = '0.0.0.0'
        port = '1911'
        status_url = 'http://{}:{}/status'.format(host, port)
        expected_startup_message = 'Mock provider started on {}:{}'.format(
            host,
            port
        )
        expected_status_json = {"status": "OK"}
        serverctl = 'mockproviderctl'

        # start server
        stdout = subprocess.check_output(
            [serverctl, '-p', port, 'start']
        )
        self.assertEqual(stdout.strip(), expected_startup_message)

        # Check server is running
        sleep(1)
        response = requests.get(status_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), expected_status_json)

        # stop server
        stdout = subprocess.check_output(
            [serverctl, 'stop']
        )
        with self.assertRaises(requests.ConnectionError):
            response = requests.get(status_url)
