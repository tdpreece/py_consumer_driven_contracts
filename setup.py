from os import path
from setuptools import setup

setup(
    name='consumer-contracts',
    packages=['consumer_contracts'],
    package_dir={'': 'src'},
    scripts=[path.join('src', 'bin', 'mockprovider')],
    install_requires=['gunicorn', 'Flask'],
    version='0.0.1',
    description='',
    author='Tim Preece',
    author_email='',
    url='',
    download_url='',
    keywords=['consumer', 'contract', 'integration', 'testing'],
    classifiers=[],
)
