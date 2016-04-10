from os import path
import re
import sys

from flask import Flask

from .blueprints.status import status_blueprint
from .blueprints.contracts import contracts_blueprint


def trim_py_extension(filename):
    return re.match('(.*)\.py', filename).groups()[0]


def create_app(contracts_path):
    app = Flask(__name__)
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
