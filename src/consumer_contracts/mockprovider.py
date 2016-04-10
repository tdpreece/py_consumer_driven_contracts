import json
from os import path
import re
import sys
from flask import Flask


def trim_py_extension(filename):
    return re.match('(.*)\.py', filename).groups()[0]

# TODO Pass this through
contracts_path = "/home/tdpreece/integration_projects/consumer_driven_contracts_using_flask/test/contracts.py"
contracts_dir = path.dirname(contracts_path)
contracts_filename = path.basename(contracts_path)
contracts_module = trim_py_extension(contracts_filename)
sys.path.append(contracts_dir)
app = Flask(__name__)
app.config.from_object(contracts_module)


@app.route('/status')
def status():
    return '{"status": "OK"}'


@app.route('/contracts')
def get_contracts():
    contracts = app.config['CONSUMER_CONTRACTS']
    contracts_list = {
        'consumer_contracts': {
            k: {u'href': u'/contracts/{}/'.format(k)}
            for k, v in contracts.items()
        }
    }
    return json.dumps(contracts_list)
