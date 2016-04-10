from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand
import sys


# From: https://tox.readthedocs.org/en/latest/example/basic.html#integration-with-setuptools-distribute-test-commands
class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


setup(
    name='consumer-contracts',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['gunicorn', 'Flask'],
    version='0.0.1',
    description='',
    author='Tim Preece',
    author_email='',
    url='',
    download_url='',
    keywords=['consumer', 'contract', 'integration', 'testing'],
    classifiers=[],
    entry_points='''
    [console_scripts]
    mockproviderctl=consumer_contracts.mockproviderctl:main
    ''',
    tests_require=['tox'],
    cmdclass={'test': Tox},
)
