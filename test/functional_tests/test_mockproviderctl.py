from os import path
import subprocess
from time import sleep
from unittest import TestCase

import requests


TEST_PORT = 1911


class MockProviderServer(object):
    def __init__(self, port, contracts_path):
        self.port = port
        self.contracts_path = contracts_path
        self.host = '0.0.0.0'
        self.serverctl = 'mockproviderctl'

    def start_server(self):
        stdout = subprocess.check_output(
            [
                self.serverctl,
                '-p',
                str(self.port),
                '-c',
                self.contracts_path,
                'start'
            ]
        )
        sleep(1)
        return stdout

    def stop_server(self):
        stdout = subprocess.check_output(
            [self.serverctl, 'stop']
        )
        return stdout

    def get(self, path, *args, **kwargs):
        url = 'http://{}:{}{}'.format(self.host, self.port, path)
        return requests.get(url, *args, **kwargs)


class TestControlOfMockProviderServer(TestCase):
    def setUp(self):
        self.port = TEST_PORT

    def test_server_starts_up_and_stops(self):
        this_dir = path.dirname(path.realpath(__file__))
        contracts_path = path.join(this_dir, 'contracts.py')
        mock_provider_server = MockProviderServer(self.port, contracts_path)
        expected_startup_message = 'Mock provider started on {}:{}'.format(
            mock_provider_server.host,
            mock_provider_server.port
        )
        status_path = '/status/'
        expected_status_json = {"status": "OK"}

        stdout = mock_provider_server.start_server()

        self.assertEqual(stdout.strip(), expected_startup_message)
        response = mock_provider_server.get(status_path)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), expected_status_json)

        stdout = mock_provider_server.stop_server()
        with self.assertRaises(requests.ConnectionError):
            response = mock_provider_server.get(status_path)


class TestLoadingAndDisplayingOfConsumerContracts(TestCase):
    def setUp(self):
        self.port = TEST_PORT
        this_dir = path.dirname(path.realpath(__file__))
        contracts_path = path.join(this_dir, 'contracts.py')
        self.mock_provider_server = \
            MockProviderServer(self.port, contracts_path)
        self.mock_provider_server.start_server()

    def tearDown(self):
        self.mock_provider_server.stop_server()

    def test_returns_consumer_contract_json(self):
        expected_contract_list_json = {
            u'consumer_contracts': {
                u'contract1': {u'href': u'/contracts/contract1/'},
                u'contract2': {u'href': u'/contracts/contract2/'},
            }
        }

        response = self.mock_provider_server.get('/contracts/')
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(response.json(), expected_contract_list_json)
