from os import path
import re
import sys

from flask import Flask

from .blueprints.status import status_blueprint
from .blueprints.contracts import contracts_blueprint


def create_app(contracts_path):
    app = MockProviderApp(contracts_path)
    return app


class MockProviderApp(Flask):
    def __init__(self, contracts_path, *args, **kwargs):
        super(MockProviderApp, self).__init__(__name__, *args, **kwargs)
        self.load_contracts_config(contracts_path)
        self.register_blueprints()

    def load_contracts_config(self, contracts_path):
        contracts_dir = path.dirname(contracts_path)
        contracts_filename = path.basename(contracts_path)
        contracts_module = trim_py_extension(contracts_filename)
        sys.path.append(contracts_dir)
        self.config.from_object(contracts_module)

    def register_blueprints(self):
        self.register_blueprint(status_blueprint, url_prefix='/status')
        self.register_blueprint(contracts_blueprint, url_prefix='/contracts')


def trim_py_extension(filename):
    return re.match('(.*)\.py', filename).groups()[0]


if __name__ == '__main__':
    app = create_app()
    app.run()
