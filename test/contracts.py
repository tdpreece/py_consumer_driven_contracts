CONSUMER_CONTRACTS = {
    'contract1': [
        {
            'request': {
                'method': 'GET',
                'path': '/x/',
            },
            'response': {
                'status': 200,
                'headers': {
                    'Content-Type': 'application/xml',
                },
                'json': {'x': 1}
            }
        }

    ],
    'contract2': [
        {
            'request': {
                'method': 'GET',
                'path': '/y/',
            },
            'response': {
                'status': 200,
                'headers': {
                    'Content-Type': 'application/xml',
                },
                'json': {'y': 2}
            }
        }

    ],
}
