# TODO
* Fix coverage
* Python 34 - double check strings

# Requirements
* A provider stub that can be used over http by consumers should be available
because consumers may not be Python projects.
* Consumer requests and associated responses should be configurable using JSON
so that the contract is easily understood by developers with no Python
background.
* When using a provider stub, a consumer should be able to set the
request/response pattern on the provider via http as part of the setup
of their tests.
* When using a provider stub, a consumer should be able to check requests
sent to the provider during the tests via http.
* consumer request/response patterns can contain a provider state parameter,
which is used to describe the state of the provider before a condumer issues
a request.
* the function used to match a consumer request to an expected request should
be configurable.

# Development
## Run tests
```python
python setup.py test
```
To pass arguments to tox,
```python
python setup.py test -a "-epy27"
```
