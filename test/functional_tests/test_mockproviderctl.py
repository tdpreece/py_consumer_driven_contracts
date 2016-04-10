from os import path
import subprocess
from time import sleep
from unittest import TestCase

import requests


class MockProviderFunctionalTest(TestCase):
    def setUp(self):
        self.host = '0.0.0.0'
        self.port = '1911'


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
                self.port,
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


class TestControlOfMockProviderServer(MockProviderFunctionalTest):
    def test_server_starts_up_and_stops(self):
        this_dir = path.dirname(path.realpath(__file__))
        contracts_path = path.join(this_dir, 'contracts.py')
        expected_startup_message = 'Mock provider started on {}:{}'.format(
            self.host,
            self.port
        )
        status_path = '/status/'
        expected_status_json = {"status": "OK"}
        mock_provider_server = MockProviderServer(self.port, contracts_path)

        stdout = mock_provider_server.start_server()

        self.assertEqual(stdout.strip(), expected_startup_message)
        response = mock_provider_server.get(status_path)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), expected_status_json)

        stdout = mock_provider_server.stop_server()
        with self.assertRaises(requests.ConnectionError):
            response = mock_provider_server.get(status_path)


class TestLoadingAndDisplayingOfConsumerContracts(MockProviderFunctionalTest):
    def test_returns_consumer_contract_json(self):
        this_dir = path.dirname(path.realpath(__file__))
        contracts_path = path.join(this_dir, 'contracts.py')
        expected_contract_list_json = {
            u'consumer_contracts': {
                u'contract1': {u'href': u'/contracts/contract1/'},
                u'contract2': {u'href': u'/contracts/contract2/'},
            }
        }
        mock_provider_server = MockProviderServer(self.port, contracts_path)
        mock_provider_server.start_server()

        response = mock_provider_server.get('/contracts/')
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(response.json(), expected_contract_list_json)

        mock_provider_server.stop_server()
