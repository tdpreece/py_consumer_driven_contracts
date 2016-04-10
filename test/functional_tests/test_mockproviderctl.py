from os import path
import subprocess
from time import sleep
from unittest import TestCase

import requests


class MockProviderFunctionalTest(TestCase):
    def setUp(self):
        self.host = '0.0.0.0'
        self.port = '1911'


class TestControlOfMockProviderServer(MockProviderFunctionalTest):
    def test_server_starts_up_and_stops(self):
        status_url = 'http://{}:{}/status/'.format(self.host, self.port)
        this_dir = path.dirname(path.realpath(__file__))
        contracts_path = path.join(this_dir, 'contracts.py')
        expected_startup_message = 'Mock provider started on {}:{}'.format(
            self.host,
            self.port
        )
        expected_status_json = {"status": "OK"}
        serverctl = 'mockproviderctl'

        # start server
        stdout = subprocess.check_output(
            [serverctl, '-p', self.port, '-c', contracts_path, 'start']
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


class TestLoadingAndDisplayingOfConsumerContracts(MockProviderFunctionalTest):
    # TODO
    # Then test that the contract returned in the json matches config file
    # Refactor:
    # - Service driver
    # - Service controller
    def test_returns_consumer_contract_json(self):
        this_dir = path.dirname(path.realpath(__file__))
        contracts_path = path.join(this_dir, 'contracts.py')
        contracts_url = 'http://{}:{}/contracts/'.format(self.host, self.port)
        expected_contract_list_json = {
            u'consumer_contracts': {
                u'contract1': {u'href': u'/contracts/contract1/'},
                u'contract2': {u'href': u'/contracts/contract2/'},
            }
        }
        serverctl = 'mockproviderctl'

        # start server
        subprocess.check_output(
            [serverctl, '-p', self.port, '-c', contracts_path, 'start']
        )

        sleep(1)
        response = requests.get(contracts_url)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(response.json(), expected_contract_list_json)

        # stop server
        subprocess.check_output(
            [serverctl, 'stop']
        )
