from os import path
import subprocess
from time import sleep
from unittest import TestCase

import requests


class TestControlOfMockProviderServer(TestCase):
    def test_server_starts_up_and_stops(self):
        host = '0.0.0.0'
        port = '1911'
        status_url = 'http://{}:{}/status/'.format(host, port)
        expected_startup_message = 'Mock provider started on {}:{}'.format(
            host,
            port
        )
        expected_status_json = {"status": "OK"}
        serverctl = 'mockproviderctl'

        # start server
        stdout = subprocess.check_output(
            [serverctl, '-p', port, '-c', 'contracts', 'start']
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


class TestLoadingAndDisplayingOfConsumerContracts(TestCase):
    # TODO
    # This test will specify a python configuration file
    # Then tests that /contracts returns a json doc lising the contracts
    # Then test that the contract returned in the json matches config file
    # Refactor:
    # - Service driver
    # - Service controller
    def test_returns_consumer_contract_json(self):
        host = '0.0.0.0'
        port = '1911'
        this_dir = path.dirname(path.realpath(__file__))
        contracts_file = path.join(this_dir)
        contracts_url = 'http://{}:{}/contracts/'.format(host, port)
        expected_contract_list_json = {
            u'consumer_contracts': {
                u'contract1': {u'href': u'/contracts/contract1/'},
                u'contract2': {u'href': u'/contracts/contract2/'},
            }
        }
        serverctl = 'mockproviderctl'

        # start server
        subprocess.check_output(
            [serverctl, '-p', port, '-c', contracts_file, 'start']
        )

        sleep(1)
        response = requests.get(contracts_url)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(response.json(), expected_contract_list_json)

        # stop server
        subprocess.check_output(
            [serverctl, 'stop']
        )
