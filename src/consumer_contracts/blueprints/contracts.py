import json

from flask import current_app, Blueprint


contracts_blueprint = Blueprint('contracts', __name__)


@contracts_blueprint.route('/')
def get_contracts():
    contracts = current_app.config['CONSUMER_CONTRACTS']
    contracts_list = {
        'consumer_contracts': {
            k: {u'href': u'/contracts/{}/'.format(k)}
            for k, v in list(contracts.items())
        }
    }
    return json.dumps(contracts_list)
