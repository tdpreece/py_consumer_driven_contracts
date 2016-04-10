import json
from os import path
import re
import sys
from flask import current_app, Blueprint, Flask


status_blueprint = Blueprint('status', __name__)
contracts_blueprint = Blueprint('contracts', __name__)


def trim_py_extension(filename):
    return re.match('(.*)\.py', filename).groups()[0]


@status_blueprint.route('/')
def status():
    return '{"status": "OK"}'


@contracts_blueprint.route('/')
def get_contracts():
    contracts = current_app.config['CONSUMER_CONTRACTS']
    contracts_list = {
        'consumer_contracts': {
            k: {u'href': u'/contracts/{}/'.format(k)}
            for k, v in contracts.items()
        }
    }
    return json.dumps(contracts_list)


def create_app():
    app = Flask(__name__)
    # TODO Pass this through
    contracts_path = "/home/tdpreece/integration_projects/consumer_driven_contracts_using_flask/test/contracts.py"
    contracts_dir = path.dirname(contracts_path)
    contracts_filename = path.basename(contracts_path)
    contracts_module = trim_py_extension(contracts_filename)
    sys.path.append(contracts_dir)
    app.config.from_object(contracts_module)
    app.register_blueprint(status_blueprint, url_prefix='/status')
    app.register_blueprint(contracts_blueprint, url_prefix='/contracts')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
